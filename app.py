import json
import threading
import queue
from flask import Flask, render_template, request, redirect, url_for, Response, flash, session
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'development-key-for-flask-session')

# Database setup
def get_db_connection():
    conn = sqlite3.connect('tickets.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
with app.app_context():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            materials TEXT NOT NULL,
            urgency TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Keep track of legacy event listeners
listeners = set()

class SSEAnnouncer:
    """Simple broadcaster for server-sent events."""

    def __init__(self):
        self.listeners = []
        self.lock = threading.Lock()

    def listen(self):
        q = queue.Queue()
        with self.lock:
            self.listeners.append(q)
        return q

    def broadcast(self, data):
        with self.lock:
            for q in list(self.listeners):
                q.put(data)

announcer = SSEAnnouncer()

def notify_listeners(ticket):
    for listener in listeners:
        listener.send_sse_data(ticket)
    announcer.broadcast(ticket)

@app.route('/events')
def events():
    def event_stream():
        listener = sse_generator()
        listeners.add(listener)
        try:
            while True:
                data = listener.get_data()
                if data:
                    yield f"data: {json.dumps(data)}\n\n"
                    yield "\n"  # Add extra newline for proper event formatting
                else:  # Send heartbeat
                    yield "data: :heartbeat\n\n"
        except GeneratorExit:
            listeners.remove(listener)
    
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/stream')
def stream():
    """SSE stream endpoint for procurement updates."""
    last_id = request.headers.get('Last-Event-ID')

    def event_stream():
        # Currently we don't store events, so missed events are ignored
        heartbeat_id = 0
        client_queue = announcer.listen()
        try:
            while True:
                try:
                    message = client_queue.get(block=True, timeout=30)
                    yield f"data: {json.dumps(message)}\n\n"
                except queue.Empty:
                    heartbeat_id += 1
                    yield f": heartbeat {heartbeat_id}\n\n"
        except GeneratorExit:
            with announcer.lock:
                if client_queue in announcer.listeners:
                    announcer.listeners.remove(client_queue)

    response = Response(event_stream(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response

class sse_generator:
    def __init__(self):
        self.queue = []
        self.event = threading.Event()

    def send_sse_data(self, data):
        self.queue.append(data)
        self.event.set()

    def get_data(self):
        self.event.wait(timeout=10)
        self.event.clear()
        return self.queue.pop(0) if self.queue else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_name = request.form['project_name']
        materials = request.form['materials']
        urgency = request.form['urgency']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tickets (project_name, materials, urgency) VALUES (?, ?, ?)',
                     (project_name, materials, urgency))
        ticket_id = cursor.lastrowid
        conn.commit()
        
        # Get the created ticket
        ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
        ticket_dict = dict(ticket)
        conn.close()
        
        # Send email and SMS notifications
        from utils.email_sender import send_ticket_notification
        send_ticket_notification(ticket_dict)
        
        # Send SMS notification if configured
        try:
            from utils.sms_sender import send_ticket_sms
            send_ticket_sms(ticket_dict, "created")
        except ImportError:
            print("SMS module not available or not configured")
            
        notify_listeners({
            'id': ticket_dict['id'],
            'title': ticket_dict['project_name'],
            'message': f"New ticket created: {ticket_dict['project_name']}"
        })
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM tickets ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/edit/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    if request.method == 'POST':
        # Get the entered PIN and the expected PIN
        entered_pin = request.form.get('pin', '')
        expected_pin = os.getenv('EDIT_PIN', '')
        
        # Check if PIN matches
        if entered_pin != expected_pin:
            print(f"PIN mismatch: entered={entered_pin}, expected={expected_pin}")
            flash('Invalid PIN. Changes not saved.', 'danger')
            return redirect(url_for('index'))
            
        # Get form data
        project_name = request.form['project_name']
        materials = request.form['materials']
        urgency = request.form['urgency']
        status = request.form['status']
        
        print(f"Updating ticket {ticket_id}: {project_name}, {urgency}, {status}")
        
        # Update the database
        conn = get_db_connection()
        conn.execute('''UPDATE tickets SET 
                        project_name = ?, 
                        materials = ?, 
                        urgency = ?, 
                        status = ?,
                        updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?''',
                     (project_name, materials, urgency, status, ticket_id))
        conn.commit()
        conn.close()
        
        # Get updated ticket data for notifications
        conn = get_db_connection()
        updated_ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
        ticket_dict = dict(updated_ticket)
        conn.close()
        
        # SMS notifications only sent for new tickets, not updates
        print("Ticket updated, no SMS notification sent as per configuration")
            
        # Send browser notification for update
        notify_listeners({
            'id': ticket_dict['id'],
            'title': ticket_dict['project_name'],
            'message': f"Ticket updated: {ticket_dict['project_name']} (Status: {ticket_dict['status']})"
        })
        
        print(f"Successfully updated ticket {ticket_id}")
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    conn.close()
    return render_template('edit.html', ticket=ticket)

@app.route('/delete/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    # Get the entered PIN and the expected PIN
    entered_pin = request.form.get('pin', '')
    expected_pin = os.getenv('EDIT_PIN', '')
    
    # Check if PIN matches
    if entered_pin != expected_pin:
        print(f"PIN mismatch on delete: entered={entered_pin}, expected={expected_pin}")
        flash('Invalid PIN. Ticket not deleted.', 'danger')
        return redirect(url_for('index'))
    
    print(f"Deleting ticket {ticket_id}")
    
    # Get ticket data before deleting for notification
    conn = get_db_connection()
    ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    ticket_dict = dict(ticket)
    
    # Delete the ticket
    conn.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()
    
    # SMS notifications only sent for new tickets, not deletions
    print("Ticket deleted, no SMS notification sent as per configuration")
        
    # Send browser notification for deletion
    notify_listeners({
        'id': ticket_dict['id'],
        'title': ticket_dict['project_name'],
        'message': f"Ticket deleted: {ticket_dict['project_name']}"
    })
    
    print(f"Successfully deleted ticket {ticket_id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Comment out SSL for testing to avoid connection issues
    # app.run(host='0.0.0.0', port=5003, debug=True, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=5003, debug=True)

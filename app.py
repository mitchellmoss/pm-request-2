from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

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
        
        # Send email notification
        from utils.email_sender import send_ticket_notification
        send_ticket_notification(ticket_dict)
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM tickets ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/edit/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    if request.method == 'POST':
        # Verify PIN
        if request.form['pin'] != os.getenv('EDIT_PIN'):
            return redirect(url_for('index'))
            
        project_name = request.form['project_name']
        materials = request.form['materials']
        urgency = request.form['urgency']
        status = request.form['status']
        
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
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    conn.close()
    return render_template('edit.html', ticket=ticket)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

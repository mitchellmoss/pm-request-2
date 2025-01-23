import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

def send_ticket_notification(ticket):
    # Configure Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates/email'))
    template = env.get_template('new_ticket.html')
    
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"New Procurement Ticket #{ticket['id']} - {ticket['project_name']}"
    msg['From'] = os.getenv('SMTP_USERNAME')
    msg['To'] = os.getenv('NOTIFICATION_EMAIL')
    
    # Render HTML template
    html = template.render(ticket=ticket)
    
    # Attach HTML version
    msg.attach(MIMEText(html, 'html'))
    
    # Create SMTP connection
    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.send_message(msg)

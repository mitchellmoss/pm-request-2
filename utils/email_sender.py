import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_email_config():
    required_vars = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'NOTIFICATION_EMAIL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def send_ticket_notification(ticket):
    try:
        # Validate environment variables
        validate_email_config()
        
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
        smtp_port = int(os.getenv('SMTP_PORT', '587'))  # Default to 587 if not set
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), smtp_port) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
            server.send_message(msg)
            print(f"Email notification sent successfully for ticket #{ticket['id']}")
            return True
            
    except ValueError as ve:
        print(f"Configuration error: {str(ve)}")
        return False
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")
        return False

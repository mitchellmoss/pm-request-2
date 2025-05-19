import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_sms_config():
    """Validate that required SMS configuration variables exist"""
    # Check if SMS is enabled
    if os.getenv('SMS_ENABLED', 'true').lower() != 'true':
        raise ValueError("SMS notifications are disabled by configuration")
        
    required_vars = ['TEXTBELT_API_KEY', 'NOTIFICATION_PHONE']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def send_ticket_sms(ticket_data, action="created"):
    """
    Send SMS notification for ticket events.
    
    Args:
        ticket_data: Dictionary containing ticket information
        action: String indicating what happened to the ticket (created, updated, deleted)
    
    Returns:
        dict: Response from TextBelt API
    """
    try:
        # Validate configuration
        validate_sms_config()
        
        # Get phone number and API key
        phone = os.getenv('NOTIFICATION_PHONE')
        api_key = os.getenv('TEXTBELT_API_KEY')
        
        # Construct message based on action
        if action == "created":
            message = f"New ticket #{ticket_data['id']} created: {ticket_data['project_name']} (Urgency: {ticket_data['urgency']})"
        elif action == "updated":
            message = f"Ticket #{ticket_data['id']} updated: {ticket_data['project_name']} (Status: {ticket_data['status']})"
        elif action == "deleted":
            message = f"Ticket #{ticket_data['id']} deleted: {ticket_data['project_name']}"
        else:
            message = f"Ticket #{ticket_data['id']} notification: {ticket_data['project_name']}"
        
        # Send SMS using TextBelt API
        resp = requests.post('https://textbelt.com/text', {
            'phone': phone,
            'message': message,
            'key': api_key,
        })
        
        # Log response
        if resp.json().get('success'):
            print(f"SMS notification sent successfully for ticket #{ticket_data['id']}")
        else:
            print(f"SMS notification failed: {resp.json().get('error')}")
        
        return resp.json()
        
    except ValueError as ve:
        print(f"SMS configuration error: {str(ve)}")
        return {"success": False, "error": str(ve)}
    except Exception as e:
        print(f"Failed to send SMS notification: {str(e)}")
        return {"success": False, "error": str(e)}
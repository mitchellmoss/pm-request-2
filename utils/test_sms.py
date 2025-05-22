import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sms_sender import send_ticket_sms, validate_sms_config

def test_sms_configuration():
    """Test SMS configuration and connection"""
    load_dotenv()
    
    print("Testing SMS configuration...")
    try:
        validate_sms_config()
        print("✓ SMS configuration is valid")
        return True
    except ValueError as e:
        print(f"✗ SMS configuration error: {e}")
        print("\nPlease set the following environment variables in your .env file:")
        print("  TEXTBELT_API_KEY - Get a key from https://textbelt.com/")
        print("  NOTIFICATION_PHONE - Phone number to send notifications to (E.164 format, e.g. +12125551234)")
        return False

def test_send_sms():
    """Test sending an SMS notification"""
    if not test_sms_configuration():
        return
    
    print("\nSending test SMS notification...")
    
    # Create a dummy ticket for testing
    test_ticket = {
        'id': 999,
        'project_name': 'Test Project',
        'urgency': 'High',
        'status': 'Pending'
    }
    
    # Test each notification type
    actions = ["created", "updated", "deleted"]
    
    for action in actions:
        print(f"\nTesting '{action}' notification:")
        response = send_ticket_sms(test_ticket, action)
        
        if response.get('success'):
            print(f"✓ Test SMS sent successfully for '{action}' action")
            print(f"  Quota remaining: {response.get('quotaRemaining', 'unknown')}")
            print(f"  Text ID: {response.get('textId', 'unknown')}")
        else:
            print(f"✗ Failed to send test SMS: {response.get('error', 'unknown error')}")

if __name__ == "__main__":
    test_send_sms()
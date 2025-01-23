from email_sender import send_ticket_notification
from datetime import datetime

def test_email_notification():
    # Create a sample ticket data
    test_ticket = {
        'id': 999,
        'project_name': 'Test Project',
        'materials': 'Test Materials',
        'urgency': 'High',
        'status': 'Pending',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Try to send the test email
    print("Attempting to send test email...")
    result = send_ticket_notification(test_ticket)
    
    if result:
        print("✅ Test email sent successfully!")
    else:
        print("❌ Failed to send test email. Please check your email configuration.")

if __name__ == "__main__":
    test_email_notification()
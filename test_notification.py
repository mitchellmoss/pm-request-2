from app import app, notify_listeners

def test_browser_notification():
    with app.test_client() as client:
        # Send a test notification
        test_data = {
            'id': 0,
            'title': 'Test Notification',
            'message': 'This is a test browser notification'
        }
        notify_listeners(test_data)
        print("✅ Test notification sent! Check your browser for the notification.")
        print("Note: Make sure you have:")        
        print("1. Enabled notifications in your browser")        
        print("2. The application running and open in your browser")        
        print("3. Clicked the '🔔 Enable Notifications' button if prompted")

if __name__ == '__main__':
    test_browser_notification()
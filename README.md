# PM-Request Ticketing System

A simple procurement request ticketing system built with Flask, SQLite, and Bootstrap.

## Features

- Create, update, and delete procurement tickets
- Track ticket status and priority
- Real-time notifications via browser notifications
- SMS notifications for ticket events
- Email notifications for new tickets
- Dark mode support
- Mobile-responsive design

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your environment variables:
   ```
   cp .env.example .env
   ```
5. Generate SSL certificates (optional, for HTTPS):
   ```
   python generate_cert.py
   ```

## Configuration

Edit the `.env` file to configure:

- `SECRET_KEY`: Flask session secret key
- `EDIT_PIN`: PIN for editing/deleting tickets
- Email settings (for email notifications):
  - `SMTP_SERVER`
  - `SMTP_PORT`
  - `SMTP_USERNAME`
  - `SMTP_PASSWORD`
  - `NOTIFICATION_EMAIL`
- SMS settings (for text message notifications):
  - `TEXTBELT_API_KEY`: Get from [TextBelt](https://textbelt.com/)
  - `NOTIFICATION_PHONE`: Phone number in E.164 format (+12125551234)

## Running the Application

Start the application:
```
python app.py
```

The application will run on port 5003 by default.

## Testing

Test email notifications:
```
python utils/test_email.py
```

Test SMS notifications:
```
python utils/test_sms.py
```

Test browser notifications:
```
python test_notification.py
```
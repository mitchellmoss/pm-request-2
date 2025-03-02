# Development Guide for PM-Request

## Commands
- Run app: `python app.py` (port 5003, SSL enabled)
- Generate SSL certificates: `python generate_cert.py`
- Test notifications: `python test_notification.py`
- Test email: `python utils/test_email.py`

## Code Style
- Imports: Standard library first, then third-party
- Naming: snake_case for functions, CapWords for classes
- Error handling: Use specific exception types in try/except blocks
- Comments: Add docstrings to functions/classes and comments for complex logic
- Environment variables: Store secrets in .env file, load with python-dotenv

## Project Structure
- Flask web app with SQLite database
- Jinja2 templates in templates/
- Static assets in static/
- Utility modules in utils/
- Email templates in templates/email/
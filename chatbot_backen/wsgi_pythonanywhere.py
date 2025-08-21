# WSGI file for PythonAnywhere
import sys
import os
from dotenv import load_dotenv

# Add your project directory to the sys.path
project_home = '/home/mandyy1223/chatbot/chatbot_backen'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Import your Flask app
from app_pythonanywhere import app as application

if __name__ == "__main__":
    application.run()

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the API token
api_token = os.getenv('JIRA_API_TOKEN')

print(api_token)  # For testing purposes only; avoid printing sensitive info in production

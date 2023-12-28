from requests_oauthlib import OAuth1Session
import webbrowser
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace these with your environment variables
client_key = os.getenv("UPWORK_API_KEY")
client_secret = os.getenv("UPWORK_SECRET")
callback_url = os.getenv("UPWORK_CALLBACK_URL")

# OAuth endpoints
request_token_url = "https://www.upwork.com/api/auth/v1/oauth/token/request"
authorize_url = "https://www.upwork.com/services/api/auth"
access_token_url = "https://www.upwork.com/api/auth/v1/oauth/token/access"

# Start the session
upwork = OAuth1Session(
    client_key, client_secret=client_secret, callback_uri=callback_url
)

# Fetch a request token
upwork.fetch_request_token(request_token_url)

# Open the authorization URL in the browser
authorization_url = upwork.authorization_url(authorize_url)
print("Please go here and authorize:", authorization_url)
webbrowser.open(authorization_url)

# Get the verifier code from the callback URL
verifier = input("Paste the verifier code here: ")

# Fetch the access token
upwork.fetch_access_token(access_token_url, verifier=verifier)

# Now you can use 'upwork' to make API calls. Here is a simple example:
response = upwork.get("https://www.upwork.com/api/auth/v1/info")
print(response.json())

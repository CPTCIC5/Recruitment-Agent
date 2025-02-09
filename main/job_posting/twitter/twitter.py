import os
import base64
import hashlib
import secrets
import requests
from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
# from users.models import User
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
load_dotenv()



# Load environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8000/api/system/auth/callback"
auth_url = "https://x.com/i/oauth2/authorize"
token_url = "https://api.x.com/2/oauth2/token"
revoke_url = "https://api.x.com/2/oauth2/revoke"

# For PKCE (Proof Key for Code Exchange) flow
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip("=")

def index(request):
    print("index running")

    # Check if 'code' exists in the request (query parameters from Twitter redirect)
    code = request.GET.get('code')
    state = request.GET.get('state')

    if code:
        print("code is present")
        # If we have an authorization code, exchange it for an access token
        return exchange_code_for_token(request, code)
    else:
        # If no code is present, redirect the user for authorization
        return redirect_to_twitter_auth(request)



def redirect_to_twitter_auth(request):
    print("redirect_to_twitter_auth running")
    # Generate the URL to redirect the user to for Twitter OAuth2 authorization
    authorization_url = f"{auth_url}?{urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'tweet.read users.read follows.read offline.access',
        'state': 'state',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'  # for method sha256
    })}"

    return HttpResponseRedirect(authorization_url)


def exchange_code_for_token(request, code: str):
    print("exchange_code_for_token running")
    # Once we have the authorization code, POST request to get the access token
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }

    # Since we're using a confidential client, we must provide credentials for authorization
    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()  # Encode to base64, format for Twitter

    headers = {
        'Authorization': f'Basic {b64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=token_data, headers=headers)

    if response.status_code == 200:
        token_info = response.json()
        ################################### SAVE THE TOKEN IN THE DATABASE ###################################
        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')
        #############################   Save the token in the database   #############################
        return JsonResponse(token_info)
    elif response.status_code == 302:
        # If the response is a redirect, it means the authorization code has expired
        return JsonResponse({'error': 'code expired, try again!'}, status=302)
    else:
        print(response.status_code)
        print(response.json())
        return JsonResponse({'error': 'Failed to exchange code for token'}, status=response.status_code)
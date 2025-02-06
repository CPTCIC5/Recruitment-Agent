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
redirect_uri = "http://127.0.0.1:8000/auth"
auth_url = "https://x.com/i/oauth2/authorize"
token_url = "https://api.x.com/2/oauth2/token"
revoke_url = "https://api.x.com/2/oauth2/revoke"

# For PKCE (Proof Key for Code Exchange) flow
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip("=")

def index(request):
    print('ran')
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        # return HttpResponseRedirect('/test') ################# CHANGE THIS TO ERROR PAGE URL #################
        return JsonResponse({'error': error}) # FOR TESTING PURPOSE

    if code:
        token_response = exchange_code_for_token(code)
        # return HttpResponseRedirect('/test') ################# CHANGE THIS TO SUCCESS PAGE URL #################
        return JsonResponse(token_response) # FOR TESTING PURPOSE

    return redirect_to_twitter_auth()

def redirect_to_twitter_auth():
    authorization_url = f"{auth_url}?{urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'tweet.read users.read follows.read offline.access',
        'state': 'state',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    })}"
    
    return HttpResponseRedirect(authorization_url)


# @login_required  ############## UNCOMMENT THIS LINE AFTER TESTING ################
def exchange_code_for_token(code: str, request):
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }

    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(token_url, data=token_data, headers=headers)
    
    if response.status_code == 200:
        token_info= response.json()
        access_token= token_info.get("access_token")
        refresh_token= token_info.get("refresh_token")
        print(token_info)
        ############################ NEED TO UNCOMMENT THIS AFTER TESTING ############################
        # user = User.objects.get(id=request.user.id)
        # organization = user.organization_set.first()
        # if organization:
        #     organization.twitter_access_token = access_token
        #     organization.twitter_refresh_token = refresh_token
        #     organization.save()
        
        return JsonResponse(token_info)
    
    else:
        return JsonResponse({'error': 'Failed to exchange code for token'}, status=response.status_code)
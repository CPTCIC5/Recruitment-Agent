import base64
import requests
from django.http import JsonResponse
from users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
revoke_url = "your_revoke_url"



@login_required
def revoke_token(request):
    user= get_object_or_404(User, id=request.user.id)  # Change logic to dynamically fetch user if needed
    organization= user.organization_set.first()
    access_token = organization.twitter_access_token or organization.twitter_refresh_token
    if not access_token:
        return JsonResponse({'error': 'Token is missing.'}, status=400)
    
    revoke_data = {'token': access_token}
    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {b64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(revoke_url, data=revoke_data, headers=headers)
    
    if response.status_code == 200:
        organization.twitter_access_token = None
        organization.twitter_refresh_token = None
        organization.save()
        return JsonResponse({'message': 'Token revoked successfully!'})
    else:
        return JsonResponse({'error': 'Failed to revoke token'}, status=response.status_code)

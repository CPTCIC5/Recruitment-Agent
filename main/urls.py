from django.urls import path
from .job_posting.twitter.twitter import index, redirect_to_twitter_auth, exchange_code_for_token

urlpatterns = [
    path('', index, name='index'),  # This now handles both redirection and exchange logic
    path('auth/', redirect_to_twitter_auth, name='auth'),  # Optional: Keep this if you need a direct URL for redirection
    path('auth/callback/', index, name='callback'),  # Handle callback from Twitter here
    path('exchange/', exchange_code_for_token, name='exchange')  # Optional: If separate URL is needed for token exchange
]

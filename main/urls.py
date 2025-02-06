from django.urls import path
from .job_posting.twitter.twitter import index,redirect_to_twitter_auth
#from job_posting.twitter.remove_token import revoke_token


urlpatterns = [
    path('', index, name='index'),
    #path('', index, name='index'),
    path('auth/', redirect_to_twitter_auth, name='auth')
]
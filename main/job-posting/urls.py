from django.urls import path
from twitter import twitter

urlpatterns = [
    path('', twitter.index, name='index'),
    path('auth/', twitter.redirect_to_twitter_auth, name='auth')
]
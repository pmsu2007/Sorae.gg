from django.urls import include, path
from django.contrib import admin
from summoner.views import TierListAPI


urlpatterns = [
    path('', TierListAPI.as_view())
]
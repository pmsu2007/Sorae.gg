from django.urls import include, path
from django.contrib import admin
from summoner.views import API
from summoner import views

urlpatterns = [
    path('', API.as_view()),
]


from django.urls import include, path
from django.contrib import admin
# from summoner.views import TierListAPI
from summoner import views


urlpatterns = [
    path('', views.search)
]
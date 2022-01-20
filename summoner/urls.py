from django.urls import include, path
from django.contrib import admin
from summoner import views
from summoner.views import API


urlpatterns = [
    path('', views.search)
    # path('', API.as_view()),
]

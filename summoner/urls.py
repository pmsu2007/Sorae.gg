from django.urls import include, path
from django.contrib import admin
from summoner import views
from summoner.views import SummonerView, MainView


urlpatterns = [
    path('', views.index),  # sorae.gg/
    path('summoner', views.search), # sorae.gg/summoner?userName
    path('validation', MainView.as_view()), # sorae.gg/validation
    path('api', SummonerView.as_view()), # sorae.gg/api
    # path('', API.as_view()),
]

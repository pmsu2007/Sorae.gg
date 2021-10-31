from django.db import models

# Create your models here.
class Tier(models.Model):
    summoner_name = models.CharField(max_length=20, primary_key=True)
    solo_tier = models.CharField(max_length=20)
    solo_rank = models.CharField(max_length=20)
    free_tier = models.CharField(max_length=20)
    free_rank = models.CharField(max_length=20)
    wins = models.IntegerField()
    losses = models.IntegerField()
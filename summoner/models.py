from django.db import models
from riotapi.SummonerData import Summoner

# Create your models here.
class Tier(models.Model):
    '''
    티어 정보
    '''
    summoner_name = models.CharField(max_length=20, primary_key=True)
    solo_tier = models.CharField(max_length=20)
    solo_rank = models.CharField(max_length=20)
    solo_wins = models.IntegerField()
    solo_losses = models.IntegerField()
    solo_leaguePoints = models.IntegerField()
    free_tier = models.CharField(max_length=20)
    free_rank = models.CharField(max_length=20)
    free_wins = models.IntegerField()
    free_losses = models.IntegerField()
    free_leaguePoints = models.IntegerField()

    def __str__(self):
        return self.summoner_name

class GameRecord(models.Model):
    '''
    경기 기록
    '''
    summoner_name = models.CharField(max_length=20, primary_key=True)
    champLevel = models.IntegerField()
    champName = models.CharField(max_length=20)
    kill = models.IntegerField()
    death = models.IntegerField()
    assist = models.IntegerField()
    CS = models.IntegerField()
    gameResult = models.BooleanField()
    playTime = models.IntegerField()

    def __str__(self):
        return self.summoner_name

class Summoner(models.Model):
    '''
    유저 정보
    '''
    summoner_name = models.CharField(max_length=20, primary_key=True)
    summoner_level = models.IntegerField()
    summoner_rank = models.IntegerField()
    summoner_icon = models.IntegerField()

    def __str__(self):
        return self.summoner_name


class UpdateDB:

    def __init__(self, userName):
        self._userName = userName

    def saveTier(self, info):
        _modelInstance = Tier(summoner_name=self._userName, solo_tier=info['solo']['tier'], solo_rank = info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])
        _modelInstance.save()

    def saveGameRecord(self, info):
        _modelInstance = GameRecord(summoner_name=self._userName, champLevel=info['champLevel'])

if __name__ == "__main__":
    DB = UpdateDB("민스님")
    DB.saveTier()
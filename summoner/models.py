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
    summoner_name = models.CharField(max_length=20, primary_key=True)  # summonerName + matchID
    champ_level = models.IntegerField()
    champ_name = models.CharField(max_length=20)
    kill = models.IntegerField()
    death = models.IntegerField()
    assist = models.IntegerField()
    CS = models.IntegerField()
    game_result = models.BooleanField()
    play_time = models.IntegerField()

    def __str__(self):
        return self.summoner_name

class Summoner(models.Model):
    '''
    유저 정보
    '''
    summoner_name = models.CharField(max_length=20, primary_key=True)
    summoner_level = models.IntegerField()
    summoner_icon = models.IntegerField()

    def __str__(self):
        return self.summoner_name


class UpdateDB:

    def __init__(self, userName):
        self._userName = userName

    def createTier(self, info):
        _modelInstance = Tier(summoner_name=self._userName, solo_tier=info['solo']['tier'], solo_rank = info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])
        _modelInstance.save()

    def createGameRecord(self, info):
        _modelInstance = GameRecord(summoner_name=self._userName+info['matchID'], champ_level=info['champLevel'],
                                    champ_name=info['champName'], kill=info['kill'], death=info['death'], assist=info['assist'],
                                    CS=info['CS'], game_result=info['gameResult'], play_time=info['playTime'])
        _modelInstance.save()

    def createSummoner(self, info):
        _modelInstance = Summoner(summoner_name=self._userName, summoner_level=info['summonerLevel']
                                  , summoner_icon=info['profileIconId'])

    def updateTier(self, info):
        _modelInstance = Tier.object.all()
        _modelInstance = _modelInstance.filter(summoner_name=self._userName)
        _modelInstance.update(solo_tier=info['solo']['tier'], solo_rank = info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])

    def updateSummoner(self, info):
        _modelInstance = Summoner.object.all()
        _modelInstance = _modelInstance.filter(summoner_name=self._userName)
        _modelInstance.update(summoner_level=info['summonerLevel'], summoner_icon=info['profileIconId'])


if __name__ == "__main__":
    DB = UpdateDB("민스님")
    DB.saveTier()
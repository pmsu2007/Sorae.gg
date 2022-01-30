from django.db import models
from riotapi.SummonerData import SummonerAPI

'''
모델 변경사항 있을 시,
makemigrations & migrate 해줘야 함
'''


class User(models.Model):
    """
    유저 정보
    summoner_name 으로 조회
    """
    summoner_name = models.CharField(max_length=20, primary_key=True)
    summoner_level = models.IntegerField()
    summoner_icon = models.IntegerField()


class Tier(models.Model):
    """
    티어 정보에 대한 테이블
    summoner_name 으로 조회
    """
    summoner_name = models.OneToOneField("User", related_name="tier", on_delete=models.CASCADE,
                                         db_column="summoner_name", primary_key=True)
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


class GameRecord(models.Model):
    """
    게임 정보 대한 테이블
    summoner_name 으로 조회
    """
    game_ID = models.CharField(max_length=30, primary_key=True)  # summonerName + matchID
    summoner_name = models.ForeignKey("User", related_name="record", on_delete=models.CASCADE,
                                      db_column="summoner_name")
    game_mode = models.CharField(max_length=20)
    champ_level = models.IntegerField()
    champ_name = models.CharField(max_length=20)
    kill = models.IntegerField()
    death = models.IntegerField()
    assist = models.IntegerField()
    CS = models.IntegerField()
    game_result = models.BooleanField()
    play_time = models.IntegerField()
    total_damage = models.IntegerField()
    vision_ward = models.IntegerField()

    class Meta:
        ordering = ['-game_ID']


class DetailRecord(models.Model):
    game_ID = models.ForeignKey("GameRecord", related_name="detail", on_delete=models.CASCADE,
                                db_column="game_ID", primary_key=True)
    primary_perk = models.IntegerField()
    sub_perk = models.IntegerField()
    item0 = models.IntegerField()
    item1 = models.IntegerField()
    item2 = models.IntegerField()
    item3 = models.IntegerField()
    item4 = models.IntegerField()
    item5 = models.IntegerField()
    item6 = models.IntegerField()
    spell1 = models.IntegerField()
    spell2 = models.IntegerField()

    class Meta:
        ordering = ['-game_ID']


class UpdateDB:
    """
    Implements CRUD about DB data
    - create Object
    DB = UpdateDB('userName')
    - use method
    UpdateDB module is used by passing the data obtained with SummonerData as parameter.
    ex) DB.createTier(info)
    """

    def __init__(self, summoner: SummonerAPI):
        self._summonerName = summoner.getName()

    def createTier(self, info):
        """
        Create record of Tier table
        """
        _modelInstance = Tier(summoner_name=User.objects.get(summoner_name=self._summonerName)
                              , solo_tier=info['solo']['tier'], solo_rank=info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])
        _modelInstance.save()

    def createGameRecord(self, info):
        """
        Create record of GameRecord table
        """
        _modelInstance = GameRecord(game_ID=self._summonerName + info['matchID'], champ_level=info['champLevel'],
                                    champ_name=info['champName'], kill=info['kill'], game_mode=info['gameMode'],
                                    death=info['death'], assist=info['assist'], CS=info['CS'],
                                    game_result=info['gameResult'], play_time=info['playTime'],
                                    summoner_name=User.objects.get(summoner_name=self._userName),
                                    total_damage=info['totalDamage'], vision_ward=info['visionWard'])
        _modelInstance.save()

    def createUser(self, info):
        """
        Create record of Summoner table
        """
        _modelInstance = User(summoner_name=info['name'], summoner_level=info['summonerLevel'],
                              summoner_icon=info['summonerIcon'])
        _modelInstance.save()

    def createDetailRecord(self, info):
        """
        Create record of DetailRecord table
        """
        _modelInstance = DetailRecord(game_ID=GameRecord.objects.get(game_ID=self._summonerName + info['matchID']),
                                      primary_perk=info['perks'][0], sub_perk=info['perks'][1],
                                      item0=info['items'][0], item1=info['items'][1], item2=info['items'][2],
                                      item3=info['items'][3], item4=info['items'][4], item5=info['items'][5],
                                      item6=info['items'][6], spell1=info['spells'][0], spell2=info['spells'][1])
        _modelInstance.save()

    def updateTier(self, info):
        """
        Update record of Tier table
        """
        _modelInstance = Tier.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=self._summonerName)
        _modelInstance.update(solo_tier=info['solo']['tier'], solo_rank=info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])

    def updateUser(self, info):
        """
        Update record of Summoner table
        """
        _modelInstance = User.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=self._summonerName)
        _modelInstance.update(summoner_level=info['summonerLevel'], summoner_icon=info['summonerIcon'])

    def deleteGameRecord(self, summonerName):
        """
        Delete all record of GameRecord table & DetailRecord table
        """
        _modelInstance = GameRecord.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=summonerName)
        _modelInstance.delete()


if __name__ == "__main__":
    DB = UpdateDB("민스님")
    DB.saveTier()

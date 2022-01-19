from django.db import models

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
    summoner_name = models.ForeignKey("User", related_name="tier", on_delete=models.CASCADE,
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
    summoner_name = models.ForeignKey("User", related_name="record", on_delete=models.CASCADE, db_column="summoner_name")
    champ_level = models.IntegerField()
    champ_name = models.CharField(max_length=20)
    kill = models.IntegerField()
    death = models.IntegerField()
    assist = models.IntegerField()
    CS = models.IntegerField()
    game_result = models.BooleanField()
    play_time = models.IntegerField()
    #






class UpdateDB:
    """
    DB 데이터에 대한 CRUD 구현

    - 객체 생성
    DB = UpdateDB('userName')
    - 메소드 사용
    Riot API로 얻은 데이터를 파라미터로 넘겨 사용
    ex)    DB.createTier(info)
    """

    def __init__(self, userName):
        self._userName = userName

    def createTier(self, info):
        """
        Tier 테이블에 레코드 생성
        """
        _modelInstance = Tier(summoner_name=User.objects.get(summoner_name=self._userName)
                              , solo_tier=info['solo']['tier'], solo_rank=info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])
        _modelInstance.save()

    def createGameRecord(self, info):
        """
        GameRecord 테이블에 레코드 생성
        """
        _modelInstance = GameRecord(game_ID=self._userName+info['matchID'], champ_level=info['champLevel'],
                                    champ_name=info['champName'], kill=info['kill'],
                                    death=info['death'], assist=info['assist'], CS=info['CS'],
                                    game_result=info['gameResult'], play_time=info['playTime'],
                                    summoner_name=User.objects.get(summoner_name=self._userName))
        _modelInstance.save()

    def createUser(self, info):
        """
        Summoner 테이블에 레코드 생성
        """
        _modelInstance = User(summoner_name=self._userName, summoner_level=info['summonerLevel'],
                              summoner_icon=info['summonerIcon'])

    def updateTier(self, info):
        """
        Tier 테이블의 user 레코드 수정
        """
        _modelInstance = Tier.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=self._userName)
        _modelInstance.update(solo_tier=info['solo']['tier'], solo_rank = info['solo']['rank']
                              , solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses']
                              , solo_leaguePoints=info['solo']['leaguePoints']
                              , free_tier=info['free']['tier'], free_rank=info['free']['rank']
                              , free_wins=info['free']['wins'], free_losses=info['free']['losses']
                              , free_leaguePoints=info['free']['leaguePoints'])

    def updateUser(self, info):
        """
        Summoner 테이블의 user 레코드 수정
        """
        _modelInstance = User.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=self._userName)
        _modelInstance.update(summoner_level=info['summonerLevel'], summoner_icon=info['summonerIcon'])


    def deleteGameRecord(self, summonerName):
        """
        GameRecord 테이블의 모든 레코드 제거
        """
        _modelInstance = GameRecord.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=summonerName)
        _modelInstance.delete()


if __name__ == "__main__":
    DB = UpdateDB("민스님")
    DB.saveTier()
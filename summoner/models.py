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
    summoner_level = models.SmallIntegerField()
    summoner_icon = models.SmallIntegerField()

    # 솔로 랭크
    solo_tier = models.CharField(max_length=20)
    solo_rank = models.CharField(max_length=20)
    solo_wins = models.SmallIntegerField()
    solo_losses = models.SmallIntegerField()
    solo_leaguePoints = models.SmallIntegerField()
    solo_progress = models.CharField(max_length=5)

    # 자유 랭크
    free_tier = models.CharField(max_length=20)
    free_rank = models.CharField(max_length=20)
    free_wins = models.SmallIntegerField()
    free_losses = models.SmallIntegerField()
    free_leaguePoints = models.SmallIntegerField()
    free_progress = models.CharField(max_length=5)


class GameRecord(models.Model):
    """
    게임 정보 대한 테이블
    summoner_name 으로 조회
    """
    game_ID = models.CharField(max_length=33, primary_key=True)  # summonerName + matchID
    match_ID = models.CharField(max_length=13)
    queue_ID = models.SmallIntegerField()                        # 420:솔로랭크, 440:자유랭크, 450:칼바람나락, 900: URF
    summoner_name = models.CharField(max_length=20)

    champ_name = models.CharField(max_length=20)
    champ_ID = models.SmallIntegerField()

    kill = models.SmallIntegerField()
    death = models.SmallIntegerField()
    assist = models.SmallIntegerField()

    game_result = models.BooleanField()
    game_duration = models.IntegerField()
    game_starttime = models.IntegerField()
    game_endtime = models.IntegerField()

    class Meta:
        ordering = ['-game_endtime']

class DetailRecord(models.Model):
    """
    한 게임 세부정보에 대한 테이블
    match_ID 으로 조회
    """
    game_ID = models.CharField(max_length=33, primary_key=True)  # summonerName + matchID
    match_ID = models.CharField(max_length=13)
    summoner_name = models.CharField(max_length=20)
    team_ID = models.SmallIntegerField()                         # (100: 블루, 200: 레드)

    minion_kill = models.SmallIntegerField()
    jungle_kill = models.IntegerField()

    champ_name = models.CharField(max_length=20)
    champ_ID = models.SmallIntegerField()
    champ_level = models.SmallIntegerField()
    total_damage = models.IntegerField()
    vision_score = models.SmallIntegerField()

    primary_rune = models.SmallIntegerField()
    sub_rune = models.SmallIntegerField()

    item0 = models.SmallIntegerField()
    item1 = models.SmallIntegerField()
    item2 = models.SmallIntegerField()
    item3 = models.SmallIntegerField()
    item4 = models.SmallIntegerField()
    item5 = models.SmallIntegerField()
    item6 = models.SmallIntegerField()

    spell1 = models.IntegerField()
    spell2 = models.IntegerField()


class UpdateDB:
    """
    Implements CRUD about DB data
    - create Object
    DB = UpdateDB('userName')
    - use method
    UpdateDB module is used by passing the data obtained with SummonerData as parameter.
    ex) DB.createTier(info)
    """

    def __init__(self, summonerName):
        self._summonerName = summonerName

    def createUser(self, info):
        """
        Create record of Summoner table
        """
        _modelInstance = User(summoner_name=info['user']['name'], summoner_level=info['user']['summonerLevel'],
                              summoner_icon=info['user']['summonerIcon'],
                              solo_tier=info['solo']['tier'], solo_rank=info['solo']['rank'],
                              solo_wins=info['solo']['wins'], solo_losses=info['solo']['losses'],
                              solo_leaguePoints=info['solo']['leaguePoints'],
                              solo_progress=info['solo']['progress'],
                              free_tier=info['free']['tier'], free_rank=info['free']['rank'],
                              free_wins=info['free']['wins'], free_losses=info['free']['losses'],
                              free_leaguePoints=info['free']['leaguePoints'],
                              free_progress=info['free']['progress'])

        _modelInstance.save()

    def createGameRecord(self, info):
        """
        Create record of GameRecord table
        """
        _modelInstance = GameRecord(game_ID=info['summonerName'] + info['matchID'],
                                    match_ID=info['matchID'], queue_ID=info['queueID'],
                                    summoner_name=self._summonerName,
                                    champ_name=info['champName'], champ_ID=info['champID'],
                                    kill=info['kill'], death=info['death'], assist=info['assist'],
                                    game_result=info['gameResult'], game_duration=info['gameDuration'],
                                    game_starttime=info['gameStartTime'], game_endtime=info['gameEndTime'])
        _modelInstance.save()

    def createDetailRecord(self, info):
        """
        Create record of DetailRecord table
        """
        _modelInstance = DetailRecord(game_ID=info['summonerName'] + info['matchID'],
                                      match_ID=info['matchID'], team_ID=info['teamID'],
                                      summoner_name=info['summonerName'],
                                      minion_kill=info['minionKill'], jungle_kill=info['jungleKill'],
                                      champ_name=info['champName'], champ_ID=info['champID'],
                                      champ_level=info['champLevel'],
                                      total_damage=info['totalDamage'], vision_score=info['visionScore'],
                                      primary_rune=info['runes'][0], sub_rune=info['runes'][1],
                                      item0=info['items'][0], item1=info['items'][1], item2=info['items'][2],
                                      item3=info['items'][3], item4=info['items'][4], item5=info['items'][5],
                                      item6=info['items'][6],
                                      spell1=info['spells'][0], spell2=info['spells'][1])
        _modelInstance.save()

    def updateUser(self, info):
        """
        Update record of Summoner table
        """
        _modelInstance = User.objects.all()
        _modelInstance = _modelInstance.get(summoner_name=self._summonerName)
        _modelInstance.summoner_level=info['summonerLevel']
        _modelInstance.summoner_icon=info['summonerIcon']
        _modelInstance.save()

    def deleteGameRecord(self, summonerName):
        """
        Delete all record of GameRecord table
        """
        _modelInstance = GameRecord.objects.all()
        _modelInstance = _modelInstance.filter(summoner_name=summonerName)
        _modelInstance.delete()

    def deleteDetailRecord(self, matchID):
        """
        Delete all record of DetailRecord table
        """
        _modelInstance = DetailRecord.objects.all()
        _modelInstance = _modelInstance.filter(match_ID=matchID)
        _modelInstance.delete()

if __name__ == "__main__":
    DB = UpdateDB("민스님")
    DB.saveTier()

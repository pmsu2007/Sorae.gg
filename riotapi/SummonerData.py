import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import requests
from riotapi.ApiConnect import ApiConnect
from summoner.models import UpdateDB
from datetime import datetime
import pprint as pp

class SummonerAPI:
    """
    Module to process data from Riot API
    """

    def __init__(self, inputName):
        self._connect = ApiConnect()
        if len(inputName) == 2:
            inputName = inputName[0] + ' ' + inputName[1]
        self._ID = self._connect.getEncryptID(inputName)

        self._summonerName = None
        if self.isValid():
            self._summonerName = self._ID['name']
            self._DB = UpdateDB(self._summonerName)
        print(self._ID)
        """
        accountId : Encrypted account ID
        id : Encrypted summoner ID
        puuid : Encrypted PUUID
        """

    def getName(self):
        """
        return summonerName
        """
        return self._summonerName

    def isValid(self):
        """
        check if response is valid
        return false if invalid data(summonerName) is input
        """
        if 'status' in self._ID.keys():
            return False
        return True

    def getTier(self):
        """
        User's Tier information
        :return: Tier information(dict)
        """
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + self._ID["id"]
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        user = self.getUser()
        solo = {'tier': "", 'rank': "", 'wins': 0, 'losses': 0, 'leaguePoints': 0, "progress": ""}
        free = {'tier': "", 'rank': "", 'wins': 0, 'losses': 0, 'leaguePoints': 0, "progress": ""}

        for rank in data:
            if rank['queueType'] == "RANKED_SOLO_5x5":
                if 'miniSeries' in rank.keys():
                    solo = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                            'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"],
                            'progress': rank['miniSeries']['progress']}
                else:
                    solo = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                            'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"],
                            'progress': ""}

            if rank['queueType'] == "RANKED_FLEX_SR":
                if 'miniSeries' in rank.keys():
                    free = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                            'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"],
                            'progress': rank['miniSeries']['progress']}
                else:
                    free = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                            'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"],
                            'progress': ""}

        info = {'user': user, 'solo': solo, 'free': free}

        self._DB.createUser(info)
        return info

    def getRecord(self, matchID):
        """
        Information about one match record
        :return: GameRecord information(dict)
        """
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        # 2021-09-01 AM 00:00:00 GMT +09:00
        MONTH = 1630422000

        if data['info']['gameStartTimestamp'] - MONTH < 0:
             return None

        if 'gameEndTimestamp' in data['info'].keys():
            '''
            2021/10/5 이후
            '''
            info = {'gameDuration': int(data['info']['gameDuration']),
                    'gameStartTime': datetime.fromtimestamp(int(data['info']['gameStartTimestamp'] / 1000)),
                    'gameEndTime': datetime.fromtimestamp(int(data['info']['gameStartTimestamp'] / 1000
                                                              + data['info']['gameDuration'])),
                    'queueID': data['info']['queueId']}

        else:
            '''
            2021/10/5 이전
            '''
            info = {'gameDuration': int(data['info']['gameDuration'] / 1000),
                    'gameStartTime': datetime.fromtimestamp(int(data['info']['gameStartTimestamp'] / 1000)),
                    'gameEndTime': datetime.fromtimestamp(int(data['info']['gameStartTimestamp'] / 1000
                                                              + data['info']['gameDuration'] / 1000)),
                    'queueID': data['info']['queueId']}

        for participant in data['info']['participants']:
            item = [participant["item0"], participant["item1"], participant["item2"], participant["item3"],
                    participant["item4"], participant["item5"], participant["item6"]]
            runes = [participant['perks']['styles'][0]['selections'][0]['perk'],
                     participant['perks']['styles'][1]['style'],
                     participant['perks']['styles'][1]['selections'][0]['perk'],
                     participant['perks']['styles'][1]['selections'][1]['perk']]
            spells = [participant['summoner1Id'], participant['summoner2Id']]
            info['assist'] = participant['assists']
            info['baron'] = participant['baronKills']
            info['champLevel'] = participant['champLevel']
            info['champName'] = participant['championName']
            info['champID'] = participant['championId']
            info['death'] = participant['deaths']
            info['dragon'] = participant['dragonKills']
            info['gameResult'] = participant['win']
            info['items'] = item
            info['jungleKill'] = participant['neutralMinionsKilled']
            info['kill'] = participant['kills']
            info['matchID'] = matchID
            info['minionKill'] = participant['totalMinionsKilled']
            info['playTime'] = participant['timePlayed']
            info['runes'] = runes
            info['summonerName'] = participant['summonerName']
            info['spells'] = spells
            info['teamID'] = participant['teamId']
            info['totalDamage'] = participant['totalDamageDealtToChampions']
            info['turret'] = participant['turretKills']
            info['visionScore'] = participant['visionScore']

            # save DetailRecord
            self._DB.createDetailRecord(info)
            # save GameRecord
            if participant['summonerName'] == self._summonerName:
                self._DB.createGameRecord(info)

        return info

    def getTotalRecord(self, start, end):
        """
        Total game record from start to end
        pass matchID as parameter to record
        :return: GameRecord informations (dictionary in list)
        """
        # start_time = time.process_time()
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
              + self._ID["puuid"] + "/ids?start=" + str(start) + "&count=" + str(end)
        response = requests.get(URL, headers=self._connect.getHeader())
        matchList = response.json()
        # end_time = time.process_time()
        # print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")
        recordList = []
        for matchID in reversed(matchList):
            try:
                recordList.append(self.getRecord(matchID))
            except KeyError:
                pass
        return recordList

    def getRecordUsingTime(self, start, end):
        """
           Total game record from startTime to endTime (timestamp)
           pass matchID as parameter to record
           :return: GameRecord informations (dictionary in list)
           """
        # start_time = time.process_time()
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
              + self._ID["puuid"] + "/ids?startTime=" + str(start) + "&endTime=" + str(end)
        response = requests.get(URL, headers=self._connect.getHeader())
        matchList = response.json()
        # end_time = time.process_time()
        # print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")

        recordList = []
        for matchID in reversed(matchList):
            try:
                recordList.append(self.getRecord(matchID))
            except KeyError:
                pass
        return recordList

    def getInGame(self):

        URL = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + self._ID['id']
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        blueTeam = []
        redTeam = []

        if 'status' in data.keys():
            return KeyError

        info = {'queueID': data['gameQueueConfigId'], 'gameStartTime': data['gameStartTime'],
                'ban': data['bannedChampions']}

        for participant in data['participants']:

            temp = {'spell': [participant['spell1Id'], participant['spell2Id']],
                    'perk': [participant['perks']['perkIds'][0], participant['perks']['perkSubStyle']],
                    'champID': participant['championId'], 'summonerName': participant['summonerName']}

            if participant['teamId'] == 100:
                blueTeam.append(temp)
            else:
                redTeam.append(temp)

        info['blue'] = blueTeam
        info['red'] = redTeam

        pp.pprint(info)

        return info


    def getUser(self):
        """
        Information about User
        :return: Summoner information(dict)
        """
        info = {'name': "", 'summonerIcon': 0, 'summonerLevel': 0}
        if self._summonerName is not None:
            info = {'name': self._ID['name'], 'summonerIcon': self._ID['profileIconId'],
                    'summonerLevel': self._ID['summonerLevel']}
        return info

    def getRenew(self):
        """
        Information about Renew
        """
        self._DB.createRenew(self._summonerName)

if __name__ == "__main__":
    summonerAPI = SummonerAPI("민스님")
    summonerAPI.getIngame()
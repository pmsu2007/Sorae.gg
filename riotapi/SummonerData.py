import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import requests
from riotapi.ApiConnect import ApiConnect
from summoner.models import UpdateDB


class SummonerAPI:
    """
    Module to process data from Riot API
    """

    def __init__(self, inputName):
        self._connect = ApiConnect()
        self._ID = self._connect.getEncryptID(inputName)

        self._summonerName = None
        if self.isValid():
            self._summonerName = self._ID['name']
            self._DB = UpdateDB(self._summonerName)

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

        info = {'gameDuration': data['info']['gameDuration'], 'gameStartTime': data['info']['gameStartTimestamp'],
                'queueID': data['info']['queueId']}

        for participant in data['info']['participants']:
            item = [participant["item0"], participant["item1"], participant["item2"], participant["item3"],
                    participant["item4"], participant["item5"], participant["item6"]]
            runes = [participant['perks']['styles'][0]['selections'][0]['perk'],
                     participant['perks']['styles'][1]['style']]
            spells = [participant['summoner1Id'], participant['summoner2Id']]
            info['assist'] = participant['assists']
            info['champLevel'] = participant['champLevel']
            info['champName'] = participant['championName']
            info['champID'] = participant['championId']
            info['death'] = participant['deaths']
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
            info['visionScore'] = participant['visionScore']

            self._DB.createDetailRecord(info)
            if participant['summonerName'] == self._summonerName:
                self._DB.createGameRecord(info)

        return info

    def getTotalRecord(self, start, end):
        """
        Total game record from start to end
        pass matchID as parameter to record
        :return: GameRecord informations (dictionary in list)
        """
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
              + self._ID["puuid"] + "/ids?start=" + str(start) + "&count=" + str(end)
        response = requests.get(URL, headers=self._connect.getHeader())
        matchList = response.json()

        recordList = []
        for matchID in reversed(matchList):
            recordList.append(self.getRecord(matchID))
        return recordList

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


if __name__ == "__main__":
    summonerAPI = SummonerAPI("rqew")
    print(summonerAPI.getTotalRecord(0, 5))

import requests
from urllib import parse
from riotapi.ApiConnect import ApiConnect
import json

class Summoner:

    def __init__(self, summonerName):
        self._connect = ApiConnect()
        self._summonerName = summonerName
        self._ID = self._connect.getEncryptID(summonerName)
        '''
        accountId : Encrypted account ID
        id : Encrypted summoner ID
        puuid : Encrypted PUUID
        '''
    def getTier(self):
        '''
        솔로랭크 & 자유랭크 정보
        tier : PLATINUM
        rank : II
        wins :  188
        loses : 167
        '''
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + self._ID["id"]
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        print(data)
        for rank in data:
            if rank['queueType'] == "RANKED_SOLO_5x5":
                solo = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                        'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"]}
            else:
                solo = {'tier': "", 'rank': "", 'wins': 0,
                        'losses': 0, 'leaguePoints': 0}
            if rank['queueType'] == "RANKED_FLEX_SR":
                free = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                        'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"]}
            else:
                free = {'tier': "", 'rank': "", 'wins': 0,
                        'losses': 0, 'leaguePoints': 0}

        info = {'solo': solo, 'free': free}
        return info

    def getRecord(self, matchID):
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        info = {}
        info['gameMode'] = data["info"]["gameMode"]

        for participant in data["info"]["participants"]:
            if participant["summonerName"] == self._summonerName:
                info['playTime'] = participant["timePlayed"]
                info['championLevel'] = participant['championLevel']
                info['championName'] = participant['championName']
                info['kill'] = participant["kills"]
                info['death'] = participant["deaths"]
                info['assist'] = participant["assists"]
                info['CS'] = participant['totalMinionsKilled']
                info['gameResult'] = participant['win']
                #item = [participant["item0"], participant["item1"], participant["item2"], participant["item3"],
                #        participant["item4"], participant["item5"], participant["item6"]]
                #info['item'] = item
                # 스펠, 같이 플레이한 소환사, 총 킬수
        return info

    def getTotalRecord(self, start, end):
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
              + self._ID["puuid"] + "/ids?start=" + str(start) + "&count=" + str(end)
        response = requests.get(URL, headers=self._connect.getHeader())
        matchList = response.json()

        recordList = []
        for matchID in matchList:
            print(matchID)
            recordList.append(self.getRecord(matchID))
        return recordList

if __name__ == "__main__":
    user = Summoner("민스님")
    print(user._ID)
    #data = user.getTier()
    #with open('myinfo.json', 'w') as f:
    #    json.dump(data, f)
    print(user.getTier())
    print(user.getTotalRecord(0,10))

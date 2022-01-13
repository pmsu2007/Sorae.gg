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
        leaguePoints : 29
        '''
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + self._ID["id"]
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        solo = {'tier': "", 'rank': "", 'wins': 0, 'losses': 0, 'leaguePoints': 0}
        free = {'tier': "", 'rank': "", 'wins': 0, 'losses': 0, 'leaguePoints': 0}

        for rank in data:
            if rank['queueType'] == "RANKED_SOLO_5x5":
                if self._summonerName in rank['summonerName']:
                    solo = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                            'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"]}

            if rank['queueType'] == "RANKED_FLEX_SR":
                if self._summonerName in rank['summonerName']:
                    free = {'tier': rank["tier"], 'rank': rank["rank"], 'wins': rank["wins"],
                            'losses': rank["losses"], 'leaguePoints': rank["leaguePoints"]}

        info = {'solo': solo, 'free': free}
        return info

    def getRecord(self, matchID):
        '''
        게임 기록 정보
        playTime : 2203 -> 60으로 나눠서 사용
        champLevel : 17
        championName : Akali
        kill : 11
        death : 6
        assist : 5
        CS : 183
        gameResult : False
        '''
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()

        info = {'playTime': 0, 'champLevel': 0, 'championName': "", 'kill': 0, 'death': 0,
                'assist': 0, 'CS': 0, 'gameResult': "" }

        for participant in data["info"]["participants"]:
            if participant["summonerName"] == self._summonerName:
                info['champLevel'] = participant['champLevel']
                info['championName'] = participant['championName']
                info['kill'] = participant["kills"]
                info['death'] = participant["deaths"]
                info['assist'] = participant["assists"]
                info['CS'] = participant['totalMinionsKilled']
                info['gameResult'] = participant['win']
                info['playTime'] = participant["timePlayed"]
                #item = [participant["item0"], participant["item1"], participant["item2"], participant["item3"],
                #        participant["item4"], participant["item5"], participant["item6"]]
                #info['item'] = item
                # 스펠, 같이 플레이한 소환사, 총 킬수
        print(info)
        return info

    def getTotalRecord(self, start, end):
        '''
        start부터 end까지 총 게임 기록
        matchID를 받아서 getRecord에 넘겨준다.
        '''
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
              + self._ID["puuid"] + "/ids?start=" + str(start) + "&count=" + str(end)
        response = requests.get(URL, headers=self._connect.getHeader())
        matchList = response.json()

        recordList = []
        for matchID in matchList:
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

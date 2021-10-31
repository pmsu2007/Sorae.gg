import requests
from urllib import parse
from backend.riotapi.ApiConnect import ApiConnect

class Summoner:

    def __init__(self, summonerName, apiKey):
        self._connect = ApiConnect(apiKey)
        self._summonerName = summonerName
        self._ID = self._connect.getEncryptID(summonerName)


    def getTier(self):
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + self._ID["id"]
        response = requests.get(URL, headers=self._connect.getHeader())
        data = response.json()
        solo = {'tier': data[0]["tier"], 'rank': data[0]["rank"], 'wins': data[0]["wins"], 'losses': data[0]["losses"]}
        free = {'tier': data[1]["tier"], 'rank': data[1]["rank"], 'wins': data[1]["wins"], 'losses': data[1]["losses"]}
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
                info['kill'] = participant["kills"]
                info['death'] = participant["deaths"]
                info['assist'] = participant["assists"]
                info['CS'] = participant['totalMinionsKilled']
                info['gameResult'] = participant['win']
                item = [participant["item0"], participant["item1"], participant["item2"], participant["item3"],
                        participant["item4"], participant["item5"], participant["item6"]]
                info['item'] = item
                # 스펠, 같이 플레이한 소환사, 총 킬수
        return info

    def getTotalRecord(self, start, end):
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" \
              + self._ID["puuid"] + "/ids?start=" + str(start) + "&count=" + str(end)
        response = requests.get(URL, headers=self._connect.getHeader())
        matchList = response.json()

        recordList = []
        for matchID in matchList:
            recordList.append(self.getRecord(matchID))

        return recordList

if __name__ == "__main__":
    user = Summoner("민스님", "RGAPI-a63e35c4-8f35-4b8e-9548-6eac3ca72d5b")
    print(user.getTier())
    print(user.getTotalRecord(0,10))

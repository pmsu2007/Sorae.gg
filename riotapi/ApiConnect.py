from urllib import parse
import requests

class ApiConnect:

    def __init__(self):
        self._apiKey = "RGAPI-d8d002f8-9c66-4bd1-9db0-17e786e08ac4"

    def getHeader (self):
        headers = {
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self._apiKey
        }
        return headers

    def getEncryptID(self, summonerName):
        encodingSummonerName = parse.quote(summonerName) # 공백을 %20으로 인코딩
        URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
        response = requests.get(URL, headers=self.getHeader())
        data = response.json()
        return data
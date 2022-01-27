from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from summoner.models import Tier, GameRecord, User, UpdateDB
from riotapi.SummonerData import SummonerAPI
from config.settings import STATIC_URL



def search(request):
    summonerName = request.GET['userName']

    summoner = SummonerAPI(summonerName)

    if not summoner.isValid() :
        return render(request, 'summoner/summoner_info.html', {'userName':summonerName, 'isValid':False})
    
    tier = summoner.getTier()

    record = summoner.getTotalRecord(0,10)

    info = {'userName': summonerName, 'tier':tier, 'record': record, 'isValid':True, 'STATIC_URL':STATIC_URL}

    return render(request,'summoner/summoner_info.html', info)


class API(APIView):

    def get(self, request):
        summonerName = request.GET['userName']  # localhost:8000/summoner?userName=민스님 //userName을 파라미터로 받는다

        # API
        summonerAPI = SummonerAPI(summonerName)
        tierData = summonerAPI.getTier()
        gameRecordData = summonerAPI.getTotalRecord(0,10)
        userData = summonerAPI.getUser()

        # DB 저장
        DB = UpdateDB(summonerName)
        DB.createUser(userData)
        DB.createTier(tierData)
        for record in gameRecordData:
            DB.createGameRecord(record)
            DB.createDetailRecord(record)

        # DB 조회
        UserquerySet = User.objects.filter(summoner_name=summonerName)

        # serializer
        serializer = UserSerializer(UserquerySet, many=True)
        return Response(serializer.data)

    def post(self, request):
        #
        # summonerName = JSONParser().parse(request)
        # print(summonerName)
        pass

    """
    DB 조회
    데이터 존재 X : 데이터 생성 -> DB 저장 -> 프론트 넘겨주기
    데이터 존재 O : 최신화 여부 확인 -> 프론트 넘겨주기기
    """

if __name__ == "__main__":
    user = SummonerAPI("민스님")
    DB = UpdateDB("민스님")
    DB.deleteGameRecord("민스님")
    print(user.getTier())
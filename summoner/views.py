from aifc import Error
from tkinter.ttk import Entry
import django
import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TierSerializer, UserSerializer, GameRecordSerializer
from summoner.models import Tier, GameRecord, User, UpdateDB
from riotapi.SummonerData import SummonerAPI
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from config.settings import STATIC_URL

def index(request):
    return render(request, 'summoner/index.html')

@csrf_exempt
def renew(request):
    # renew profile

    summonerName = json.loads(request.body).get('userName')
    summoner = SummonerAPI(summonerName)
    summonerName = summoner.getName()

    if not summoner.isValid() :
        return JsonResponse({'status':400})
    
    # Data 생성
    tierData = summoner.getTier()
    gameRecordData = summoner.getTotalRecord(0, 10)
    userData = summoner.getUser()

    # DB 갱신
    DB = UpdateDB(summoner)

    DB.createUser(userData)
    DB.createTier(tierData)
    for record in reversed(gameRecordData):
        DB.createGameRecord(record)
        DB.createDetailRecord(record)

    return JsonResponse({'status':200})

class SummonerView(APIView):

    def get(self, request):

        # URL : sorae.gg/api?userName
        inputName = request.GET['userName']
        summoner = SummonerAPI(inputName)
        summonerName = summoner.getName()

        if not summoner.isValid() :
            return render(request, 'summoner/summoner_info.html', {'userName':inputName})
        
        # DB 조회
        # alternative : get_object_or_404(User, summoner_name=summonerNmae)
        try:
            userQuery = User.objects.get(summoner_name=summonerName)
        except ObjectDoesNotExist:
            """
            if Data dosen't exist then create DB
            """
            # Data 생성
            tierData = summoner.getTier()
            gameRecordData = summoner.getTotalRecord(0, 10)
            userData = summoner.getUser()

            # DB 저장
            DB = UpdateDB(summoner)

            DB.createUser(userData)
            DB.createTier(tierData)
            for record in reversed(gameRecordData):
                DB.createGameRecord(record)
                DB.createDetailRecord(record)
          

        # serializer
        userQuery = User.objects.get(summoner_name=summonerName)
        tierQuery = Tier.objects.get(summoner_name=summonerName)
        recordQuery = GameRecord.objects.filter(summoner_name=summonerName)
        userSerialize = UserSerializer(userQuery)
        tierSerialize = TierSerializer(tierQuery)
        gameRecordSerialize = GameRecordSerializer(recordQuery, many=True)

        return render(request, 'summoner/summoner_info.html',
                      {'user': userSerialize.data, 'tier': tierSerialize.data, 'gameRecord': gameRecordSerialize.data
                          , 'STATIC_URL': STATIC_URL})

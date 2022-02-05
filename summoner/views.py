import django
import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, GameRecordSerializer, DetailRecordSerializer
from summoner.models import GameRecord, User, DetailRecord, UpdateDB
from riotapi.SummonerData import SummonerAPI
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from config.settings import STATIC_URL
from datetime import datetime


def index(request):
    return render(request, 'summoner/index.html')

@csrf_exempt
def renew(request):
    # renew profile

    summonerName = json.loads(request.body).get('userName')
    summoner = SummonerAPI(summonerName)
    summonerName = summoner.getName()

    if summonerName == None :
        return JsonResponse({'status':400})
    
    # Data 갱신
    tierData = summoner.getTier()
    gameRecordData = summoner.getTotalRecord(0, 20)

    return JsonResponse({'status':200})

class SummonerView(APIView):

    def get(self, request):

        # URL : sorae.gg/summoner?userName
        inputName = request.GET['userName']
        summoner = SummonerAPI(inputName)
        summonerName = summoner.getName()

        # 소환사 이름이 없을때
        if summonerName == None :
            return render(request, 'summoner/summoner_info.html', {'userName':inputName})
        
        # DB 조회
        # alternative : get_object_or_404(User, summoner_name=summonerNmae)
        try:
            userQuery = User.objects.get(summoner_name=summonerName)
        except ObjectDoesNotExist:
            """
            if Data dosen't exist then create DB
            """
            # Data 생성 및 저장
            tierData = summoner.getTier()
            gameRecordData = summoner.getTotalRecord(0, 20) # 20 게임 불러오기

        # serializer
        userQuery = User.objects.get(summoner_name=summonerName)
        recordQuery = GameRecord.objects.filter(summoner_name=summonerName)[:20]
        userSerialize = UserSerializer(userQuery)
        gameRecordSerialize = GameRecordSerializer(recordQuery, many=True)
        
        return render(request, 'summoner/summoner_info.html',
                      {'user': userSerialize.data, 'record': gameRecordSerialize.data
                          , 'STATIC_URL': STATIC_URL})

class MainView(APIView):

    def post(self, request):

        inputName = request.POST.get("userName")

        API = SummonerAPI(inputName)
        summonerName = API.getName()

        if API.isValid():

            API.getTier()
            API.getTotalRecord(0, 10)
            return Response(data={'status': 200})
        else:
            return Response(data={'status': 404})

class DetailView(APIView):

    def post(self, request):

        matchID = request.POST.get("matchID")
        summonerName = request.POST.get("userName")
        summoner = SummonerAPI(summonerName)

        # DB 조회
        try:
            # GameRecord에 동일한 matchID가 있다면 생성할 필요 없음
            recordQuery = GameRecord.objects.get(match_ID=matchID)
        except ObjectDoesNotExist:
            # Data 생성 및 저장
            summoner.getRecord(matchID)

        # serializer
        detailQuery = DetailRecord.objects.filter(match_ID=matchID)
        detailRecordSerializer = DetailRecordSerializer(detailQuery, many=True)

        return Response(detailRecordSerializer.data)
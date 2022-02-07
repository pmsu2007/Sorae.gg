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
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from config.settings import STATIC_URL
from datetime import datetime
from django.views import View
import time


def index(request):
    return render(request, 'summoner/index.html')


class SummonerView(View):

    def get(self, request):

        # URL : sorae.gg/summoner?userName
        inputName = request.GET['userName']
        summoner = SummonerAPI(inputName)
        summonerName = summoner.getName()

        # 소환사 이름이 없을때
        if summonerName == None:
            return render(request, 'summoner/summoner_info.html', {'userName': inputName})

        # DB 조회
        # alternative : get_object_or_404(User, summoner_name=summonerNmae)
        try:
            userQuery = User.objects.get(summoner_name=summonerName)
            # gameRecordData = summoner.getTotalRecord(0, 20)
        except ObjectDoesNotExist:
            """
            if Data dosen't exist then create DB
            """
            # Data 생성 및 저장
            tierData = summoner.getTier()
            gameRecordData = summoner.getTotalRecord(0, 20)
            userQuery = User.objects.get(summoner_name=summonerName)
        # serializer
        recordQuery = GameRecord.objects.filter(summoner_name=summonerName)[:20]  # 20 게임 불러오기
        userSerialize = UserSerializer(userQuery)
        gameRecordSerialize = GameRecordSerializer(recordQuery, many=True)

        return render(request, 'summoner/summoner_info.html',
                      {'user': userSerialize.data, 'record': gameRecordSerialize.data
                          , 'STATIC_URL': STATIC_URL})

    def post(self, request):
        '''
        renew summoner's info
        '''
        # try:
        summonerName = json.loads(request.body).get('userName')
        summoner = SummonerAPI(summonerName)
        summonerName = summoner.getName()

        if summonerName == None:
            return JsonResponse({'status': 400})

        userQuery = User.objects.get(summoner_name=summonerName)
        curTime = int(time.mktime(datetime.now().timetuple()))
        lastRecordQuery = GameRecord.objects.filter(summoner_name=summonerName)[0]
        lastMatchTime = int(time.mktime(lastRecordQuery.game_end.timetuple()))
        # print(datetime.fromtimestamp(curTime/1000))
        # print(datetime.fromtimestamp(lastMatchTime/1000))
        # Data 갱신
        tierData = summoner.getTier()
        gameRecordData = summoner.getRecordUsingTime(lastMatchTime, curTime)

        return JsonResponse({'status': 200})
        # except Exception:
        #     return JsonResponse({'status':400})


class DetailView(View):

    def post(self, request):

        # data = json.loads(request.body)

        # Postman
        summonerName = request.POST['userName']
        matchID = request.POST['matchID']
        # API
        summoner = SummonerAPI(summonerName)
        # DB 조회
        try:
            # GameRecord에 동일한 matchID가 있다면 생성할 필요 없음
            recordQuery = GameRecord.objects.get(match_ID=matchID)
        except ObjectDoesNotExist:
            # Data 생성 및 저장
            detailData = summoner.getRecord(matchID)

        # serializer
        detailQuery = DetailRecord.objects.filter(match_ID=matchID)
        detailRecordSerialize = DetailRecordSerializer(detailQuery, many=True)

        return JsonResponse(detailRecordSerialize.data, status=200, safe=False)

from urllib import response
import django
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import UserSerializer, GameRecordSerializer, DetailRecordSerializer
from summoner.models import GameRecord, User, DetailRecord, Renew, UpdateDB
from riotapi.SummonerData import SummonerAPI
from django.core.exceptions import ObjectDoesNotExist
from config.settings import STATIC_URL
from datetime import datetime
from django.views import View
from django.template import loader
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
            renewData = summoner.getRenew()
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
        try:
            summonerName = json.loads(request.body).get('userName')
            summoner = SummonerAPI(summonerName)
            summonerName = summoner.getName()

            if summonerName == None:
                return JsonResponse({'status': 400})

            curTime = int(time.mktime(datetime.now().timetuple()))
            lastRecordQuery = GameRecord.objects.filter(summoner_name=summonerName)[0]
            lastMatchTime = int(time.mktime(lastRecordQuery.game_end.timetuple()))

            # Data 갱신
            tierData = summoner.getTier()
            gameRecordData = summoner.getRecordUsingTime(lastMatchTime, curTime)

            # 전적 시간 갱신
            renewQuery = Renew.objects.get(summoner_name=summonerName)
            renewQuery.renew_time = time.mktime(datetime.today().timetuple())
            renewQuery.save()

            return JsonResponse({'status': 200})

        except Exception:
            return JsonResponse({'status':400})


class DetailView(View):

    def get(self, request):

        matchID = request.GET['matchID']

        # serializer
        try:
            detailQuery = DetailRecord.objects.filter(match_ID=matchID)
            detailRecordSerialize = DetailRecordSerializer(detailQuery, many=True)
            data = detailRecordSerialize.data
            blue_team = data[:5]
            red_team = data[5:]
            res = loader.render_to_string('summoner/record_detail.html', {'blue':blue_team, 'red':red_team})
            # return render(None, 'summoner/record_detail.html', {'blue':blue_team, 'red':red_team})
            return JsonResponse({'data':res})

        except ObjectDoesNotExist:
            return JsonResponse({'message': "Not Found Match ID"}, status=404)

class RenewView(View):

    def get(self, request):
        inputName = request.GET['userName']

        #API
        summoner = SummonerAPI(inputName)
        summonerName = summoner.getName()

        # DB 조회
        try:
            renewQuery = Renew.objects.get(summoner_name=summonerName)
            return JsonResponse(int(renewQuery.renew_time), status=200, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'message': "Not Found Summoner"}, status=404)
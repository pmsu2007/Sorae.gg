from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TierSerializer
from .models import Tier, UpdateDB
from riotapi.SummonerData import Summoner
from django.shortcuts import render


# class TierListAPI(APIView):

#     def get(self, request):
#         summonerName = request.GET['userName']  # localhost:8000/summoner?userName=민스님 //userName을 파라미터로 받는다

#         summoner = Summoner(summonerName)
#         data = summoner.getTier()
#         DB = UpdateDB(summonerName)
#         DB.saveTier(data)

#         TierquerySet = Tier.objects.all()
#         TierquerySet = TierquerySet.filter(summoner_name=summonerName)

#         serializer = TierSerializer(TierquerySet, many=True)
#         return Response(serializer.data)

def search(request):
    summonerName = request.GET['userName']

    summoner = Summoner(summonerName)

    if not summoner.isValid() :
        return render(request, 'summoner/summoner_info.html', {'userName':summonerName})
    
    tier = summoner.getTier()

    record = summoner.getTotalRecord(0,10)

    info = {'userName': summonerName, 'tier':tier, 'record': record}

    return render(request,'summoner/summoner_info.html', info)


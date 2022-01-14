from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TierSerializer
from .models import Tier, UpdateDB
from riotapi.SummonerData import Summoner


class TierListAPI(APIView):

    def get(self, request):
        summonerName = request.GET['userName']  # localhost:8000/summoner?userName=민스님 //userName을 파라미터로 받는다

        summoner = Summoner(summonerName)
        data = summoner.getTier()
        DB = UpdateDB(summonerName)
        DB.saveTier(data)

        TierquerySet = Tier.objects.all()
        TierquerySet = TierquerySet.filter(summoner_name=summonerName)

        serializer = TierSerializer(TierquerySet, many=True)
        return Response(serializer.data)


if __name__ == "__main__":
    user = Summoner("민스님")
    print(user.getTier())

from rest_framework import serializers
from .models import Tier, GameRecord, User

# Serializer를 선언할 때는 데이터 형태에 대한 필드, 데이터를 처리할 메소드가 필요
# ModelSerializer는 위의 내용들을 알아서 해준 형태의 Serializer이다.


class GameRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRecord
        fields = '__all__'


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    record = GameRecordSerializer(many=True, read_only=True)
    tier = TierSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

from rest_framework import serializers
from .models import Tier

# Serializer를 선언할 때는 데이터 형태에 대한 필드, 데이터를 처리할 메소드가 필요
# ModelSerializer는 위의 내용들을 알아서 해준 형태의 Serializer이다.

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier        # Tier 모델 사용
        fields = '__all__'  # 모든 필드 포함

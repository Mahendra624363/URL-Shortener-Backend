from rest_framework import serializers
from .models import UrlData

class UrlDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlData
        fields = ["id", "original_url", "short_code", "created_at", "clicks"]
        read_only_fields = ["id", "short_code", "created_at", "clicks"]

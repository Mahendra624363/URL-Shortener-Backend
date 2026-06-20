from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import UrlData
from .serializers import UrlDataSerializer

BASE64_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

def encode_id(num):
    if num == 0:
        return BASE64_ALPHABET[0]

    base = 64
    encoded = ""

    while num > 0:
        remainder = num % base
        encoded = BASE64_ALPHABET[remainder] + encoded
        num = num // base

    return encoded

def decode_id(code):
    base = 64
    num = 0

    for char in code:
        num = num * base + BASE64_ALPHABET.index(char)

    return num

class UrlShortenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user=request.user
        if user.count>=10:
            return Response({"message":"user exceeded 10 links generator"}, status=400)
        serializer = UrlDataSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()

            obj.short_code = encode_id(obj.id)
            obj.save()

            return Response({
                "id": obj.id,
                "original_url": obj.original_url,
                "short_code": obj.short_code,
                "short_url": request.build_absolute_uri(f"/{obj.short_code}/"),
                "clicks": obj.clicks
            },status=201)

        return Response(serializer.errors, status=400)
    
class RedirectUrlView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, code):
        try:
            pk = decode_id(code)  
        except Exception:
            return Response({"detail": "Invalid code"}, status=400)

        obj = get_object_or_404(UrlData, id=pk)

        obj.clicks += 1
        obj.save()

        return redirect(obj.original_url)
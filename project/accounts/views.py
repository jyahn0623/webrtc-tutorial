from django.shortcuts import render
from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
import json
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

""" OTP 관련 코드 """
# 유저의 디바이스를 가지고 옴
def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

# 유저의 TOTP를 생성함
class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)

# 유저에 발급된 TOTP가 유효한지 확인함
class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return Response(True, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAPI(views.APIView):

    def post(self, requset):
        datas = json.loads(requset.body)
        user = User.objects.create_user(
            username=datas.get('username'),
            email=datas.get('email'),
            password=datas.get('password')
        )

        token = Token.objects.create(user=user)
        return Response(status=200)


class UserLogin(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        return Response({
            'token' : token.key
        })


# $ curl -X GET -H 'Authorization: Token fe64c4963c312e8a924096ff6b14ff91d2150b5a' -i localhost:8000/api/totp/create/ 
# OTP 디바이스 등록

"""

"""
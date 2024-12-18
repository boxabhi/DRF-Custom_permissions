from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FileUploaderSerializer, OrderSerializer,FileUploader
from .excelReader import handleExcelUpload
from django.conf import settings
from .models import Order
from .rate_limiter import rate_limit
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from .permission_checker import check_permission


class LoginAPI(APIView):
    def post(self , request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username = username, password = password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "status" : True,
                "message" : "token",
                "data" : str(token)
            })
        return Response({
                "status" : False,
                "message" : "in valid",
                "data" : None
            })
    





class ExcelUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    @check_permission("POST", FileUploader)
    @rate_limit(max_requests=15, time_window=60 * 5)
    def post(self , request):
        return Response({
                "status" : True,
                "message" : "File uploaded"
            })
        
        data = request.data
        serializer = FileUploaderSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.data['file']
            print(file_path)
            handleExcelUpload(f"{settings.BASE_DIR}/{file_path}")
            return Response({
                "status" : True,
                "message" : "File uploaded"
            })
        
        return Response({
                "status" : False,
                "message" : "File not uploaded",
                "data" : serializer.errors
            })



class OrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


    @check_permission("GET", Order)
    @rate_limit(max_requests=15, time_window=60 * 5)
    def get(self ,request):
        orders = Order.objects.all()[:10]
        serializer = OrderSerializer(orders, many = True)
        return Response({
                "status" : True,
                "message" : "orders",
                "data" : serializer.data
            })

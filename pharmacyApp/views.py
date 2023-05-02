from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, status
from .models import*
from .serializers import*
# Create your views here.

# this fun gets from doctors or add a new doctors
@api_view(['GET','POST'])
def get_Aadd_Doctor(request): 
    if request.method =='GET':
        doctors  = Doctor.objects.all()
        serializer = DoctorSerializer(doctors,many =True)
        return JsonResponse(serializer.data, status = status.HTTP_200_ok)
    if request == 'POST':
        return  Response({'message':'the method is not allowed', 'status':status.HTTP_405_METHOD_NOT_ALLOWED})
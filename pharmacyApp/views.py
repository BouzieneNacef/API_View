import datetime
from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import*
from .serializers import*
# Create your views here.

# this fun gets from doctors or add a new doctors
@api_view(['GET','POST'])
def get_Add_Doctor(request): 
    if request.method =='GET':
        doctors  = Doctor.objects.all()
        serializer = DoctorSerializer(doctors,many =True)
        return JsonResponse(serializer.data, status = status.HTTP_200_ok)
    if request == 'POST':
        return  Response({'message':'the method is not allowed', 'status':status.HTTP_405_METHOD_NOT_ALLOWED})

 #the patients of a given doctor:   
@api_view(['GET'])
def doctor_patients_list(request, doctor_id):
    try:
        doctor = Doctor.objects.get(pk = doctor_id)
        patient = Patient.objects.filter(doctor=doctor)
        serializer = PatientSerializer(patient, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response({'error':'Doctor does not exist.'}, status=status.HTTP_404_NOT_FOUND)

# the turnover for a given pharmacist during a given week:  
@api_view(['GET'])
def pharmacist_weekly_sales(request, pharmacist_id, week_start_date):
    try:
        pharmacist = Pharmacist.objects.get(pk=pharmacist_id)
        week_end_date = datetime.strptime(week_start_date, '%Y-%m-%d') + datetime.timedelta(days=7)
        weekly_sales = Prescription.objects.filter(pharmacist=pharmacist, date__range=[week_start_date, week_end_date]).aggregate(Sum('total_price'))['total_price__sum']
        if weekly_sales is None:
            weekly_sales = 0
        return Response({'weekly_sales': weekly_sales}, status=status.HTTP_200_OK)
    except Pharmacist.DoesNotExist:
        return Response({'error': 'Pharmacist does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
# the most requested drug:
@api_view(['GET'])
def most_demanded_drug(request):
    drug_sales = PrescriptionDrug.objects.values('drug__name').annotate(total=Sum('quantity')).order_by('-total')
    most_demanded_drug = drug_sales.first()
    return Response({'drug_name': most_demanded_drug['drug__name'], 'total_quantity_sold': most_demanded_drug['total']})

# the prescriptions of a given doctor served by a given pharmacist:
@api_view(['GET'])
def prescriptions_by_doctor_and_pharmacist(request, doctor_id, pharmacist_id):
    prescriptions = Prescription.objects.filter(doctor_id=doctor_id, pharmacist_id=pharmacist_id)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response(serializer.data)
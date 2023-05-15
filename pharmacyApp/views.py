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
# we have one url for both options
# url= http://localhost:8000/api/doctor/
# if you use GET method you will get a new doctor
# if you use POST method you will add a new doctor
@api_view(['GET','POST'])
def get_Add_Doctor(request): 
    if request.method =='GET':
        doctors  = Doctor.objects.all()
        serializer = DoctorSerializer(doctors,many =True)
        return JsonResponse(serializer.data, status = status.HTTP_200_ok)
    if request == 'POST':
        serializer = DoctorSerializer(data=request.data)
        # verify if passed is valid
        # the data is not valid if for exemple the email is not well formatted
        if serializer.is_valid():
            # add the doctor to the database
            serializer.save()
            # the data return a json data
            return JsonResponse({'message':'you have to use POST or GET'}, status= status.HTTP_201_CREATED)
        # if the data retuen yhe error
        return JsonResponse(serializer.data, status = status.HTTP_400_BAD_REQUEST)
    return  Response({'message':'the method is not allowed', 'status':status.HTTP_405_METHOD_NOT_ALLOWED})

#this function get all doctor patients or delete all of them :
@api_view(['GET','DELETE'])
def get_doctor_patients(request,doctor_id):
        
        doctor1=Doctor.objects.get(pk=doctor_id)
        if doctor1 is None:
            return JsonResponse({'message':f'Doctor with id = {doctor_id} not found'},status=status.HTTP_404_NOT_FOUND)

        patients=Prescription.objects.filter(doctor=doctor1)
        if request.method=='GET':
            serializer=PatientSerializer(patients,many=True)
            #serializer.data allows to get the data in json format after serialization
            return JsonResponse(serializer.data,status=status.HTTP_200_OK, safe= False)
        elif request.method=='DELETE':
            for patient in patients:
                patient.delete()
            return JsonResponse({'message':f'All patients of doctor with id = {doctor_id} are deleted'},status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message':'You have to use GET or DELETE'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
from . import views
from django.urls import path


urlpatterns = [
    path(r'doctor/', views.get_Add_Doctor, name='doctor'),
    path(r'doctor/<int:doctor_id>/pations/', views.get_doctor_patients, name='patients_by_doctor'),
    path(r'pharmacist-weekly/<int:pharmacist_id>/<str:date>/', views.pharmacist_weekly_sales, name='pharmacist_revenue'),
    path(r'most-demanded-drug/', views.most_demanded_drug, name='most_demanded_drug'),
    path(r'prescriptions/<int:doctor_id>/<int:pharmacist_id>/', views.prescriptions_by_doctor_and_pharmacist, name='prescriptions_by_doctor_and_pharmacist'),
]

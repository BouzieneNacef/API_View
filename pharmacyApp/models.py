from django.db import models


# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=20, default='')
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=20)
    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.name

class Pharmacist(models.Model):
    name = models.CharField(max_length=20, default='')
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=20)
    class Meta:
        db_table = 'pharmacist'

class Patient(models.Model):
    name = models.CharField(max_length=20, default='')
    email=models.EmailField(max_length=254,unique=True,default='')
    phone=models.CharField(max_length=20,null=True,blank=True)
    class Meta:
        db_table = 'patient'
        #Patients are ordered by lastName and email in descending order

class Drug(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    manufacturingDate=models.DateField(null=True,blank=True)
    expirationDate=models.DateField(null=True,blank=True)
    stock=models.PositiveIntegerField(default=0)
    description=models.TextField(null=True,blank=True)
    photo=models.ImageField(upload_to='photos',null=True,blank=True)
    class Meta:
        db_table = 'drug'

class Prescription(models.Model):
     drug=models.ManyToManyField(Drug, through='PrescriptionDrug', through_fields=('prescription', 'drug'))
     doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
     patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
     drug=models.ForeignKey(Drug,on_delete=models.CASCADE)
     pharmacist=models.ForeignKey(Pharmacist,on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField(default=0)
     class Meta:
        db_table = 'Prescription'

class PrescriptionDrug(models.Model):
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug,on_delete=models.CASCADE)
    quantity= models.PositiveBigIntegerField(default=0)
    consoming_duration = models.DurationField(null= True, blank=True) # n'est pas obligataire


     
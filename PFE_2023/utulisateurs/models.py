from django.db import models
from django.contrib.auth.models import AbstractUser , PermissionsMixin, Group , Permission
from utulisateurs.manager import UserManager
# Create your models here.
from django.contrib.auth.models import User
import random


class User(AbstractUser, PermissionsMixin):
    ROLES = (
        ('directeur-regional', 'Directeur-Regional'),
        ('responsable-center', 'Responsable-Center'),
        ('patient', 'Patient'),
    )
    num = random.random()
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLES, max_length=20, default='patient')
    nni = models.CharField(max_length=20,default=num)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    def __str__(self):
        return self.role + ", " + self.email

class Wilaya(models.Model):
    nom = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nom

class Moughataa(models.Model):
    nom = models.CharField(max_length=50)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class CentreDeVaccination(models.Model):
    nom = models.CharField(max_length=50)
    moughataa = models.ForeignKey('Moughataa', on_delete=models.CASCADE, default='tgnt')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class AdminCenter(models.Model):
    TYPE = (
        ('admin', 'Admin'),
        ('professionnel','Professionnel'),
        ('gerent-stock','Gerent-Stock')
    )
    center = models.OneToOneField(CentreDeVaccination, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE,max_length=15,default='admin')

class TypeVaccination(models.Model):
    CATEGORIE = (
        ('enfants', 'Enfants'),
        ('jeunes-femmes', 'Jeunes-Femmes'),
        ('jeunes-hommes', 'Jeunes-Hommes'),
        ('veux', 'Veux'),
        ('tout-monde', 'Tout-Monde')
    )
    nom = models.CharField(max_length=50)
    categorie = models.CharField(choices=CATEGORIE, max_length=50)

'''class Vaccine(models.Model):
    nom = models.CharField(max_length=100)
    type = models.OneToOneField(TypeVaccination, on_delete=models.CASCADE)
    fabricant = models.CharField(max_length=50)
    doses_administrées = models.IntegerField()
    total_doses = models.IntegerField()
    
'''
class Vaccine(models.Model):
    nom = models.CharField(max_length=100)
    total_doses = models.IntegerField()
    type = models.ForeignKey(TypeVaccination, on_delete=models.CASCADE)
    fabricant = models.CharField(max_length=50)
    doses_administrées = models.IntegerField()


class Dose(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='doses')
    number = models.IntegerField(default=1)
    durée = models.DurationField()



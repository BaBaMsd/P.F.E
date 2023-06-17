from django.db import models
from django.contrib.auth.models import AbstractUser , PermissionsMixin, Group , Permission
from utulisateurs.manager import UserManager
# Create your models here.
from django.contrib.auth.models import User
import random
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
import  qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File


class User(AbstractUser, PermissionsMixin):
    ROLES = (
        ('responsable-center', 'Responsable-Center'),
        ('patient', 'Patient'),
        ('professionnel','Professionnel'),
        ('gerent-stock','Gerent-Stock')
    )
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLES, max_length=20, default='patient')
    nni = models.CharField(max_length=20,default='')


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    
    objects = UserManager()
    def __str__(self):
        return self.role + ", " + self.email

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def _str_(self):
        return f'{self.user.email} Profile'

    def save(self, *args, **kwargs):
        kwargs.setdefault('force_insert', False)
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Wilaya(models.Model):
    code = models.CharField(max_length=2)
    nom = models.CharField(max_length=50)    
    def __str__(self):
        return self.nom

class Moughataa(models.Model):
    nom = models.CharField(max_length=50)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class CentreDeVaccination(models.Model):
    nom = models.CharField(max_length=50)
    moughataa = models.ForeignKey('Moughataa', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.nom

class AdminCenter(models.Model):
    TYPE = (
        ('admin', 'Admin'),
        ('professionnel','Professionnel'),
        ('gerent-stock','Gerent-Stock')
    )
    center = models.ForeignKey(CentreDeVaccination, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE,max_length=15,default='admin')

    def __str__(self):
        return f'{self.center.nom} {self.type}'




class TypeVaccination(models.Model):
    SEXE=[
        ('homme','Homme'),
        ('femme','Femme')
    ] 
    nom = models.CharField(max_length=100)
    description = models.TextField(default='')
    sexe_cible = models.CharField(choices=SEXE,max_length=10,default='femme')
    age_minimum = models.IntegerField(default=1)
    age_maximum = models.IntegerField(default=100)

    def __str__(self):
        return self.nom    

class Vaccine(models.Model):
    nom = models.CharField(max_length=100)
    total_doses = models.IntegerField()
    type = models.ForeignKey(TypeVaccination, on_delete=models.CASCADE)
    fabricant = models.CharField(max_length=50)
    doses_administrées = models.IntegerField()

    def __str__(self):
        return self.nom


class Dose(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='doses')
    number = models.IntegerField(default=1)
    duree = models.IntegerField()
    def __str__(self):
        return f'{self.vaccine.nom} dose: {self.number}  '


class StockVaccins(models.Model):
    OPERATION_CHOICES = [
        ('AJOUTER', 'Addition'),
        ('SUPRIMER', 'Suppresion'),
    ]
    typeOperation = models.CharField(max_length=15, choices=OPERATION_CHOICES)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    dateExpiration = models.DateField()
    dateOperation = models.DateTimeField(auto_now_add=True)
    centerVaccination = models.ForeignKey(CentreDeVaccination, on_delete=models.CASCADE)
    numeroLot = models.CharField(max_length=50, default='I18207')

    def __str__(self):
        return f'{self.vaccine.nom} {self.centerVaccination.nom}  '


class HistoriqueStock(models.Model):
    OPERATION_CHOICES = [
        ('AJOUTER', 'Addition'),
        ('SUPRIMER', 'Suppresion'),
    ]
    typeOperation = models.CharField(max_length=15)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    dateExpiration = models.DateField()
    dateOperation = models.DateTimeField(auto_now_add=True)
    centerVaccination = models.ForeignKey(CentreDeVaccination, on_delete=models.CASCADE)
    numeroLot = models.CharField(max_length=50, default='I18207')

    def __str__(self):
        return f'{self.vaccine.nom} {self.centerVaccination.nom}  '




#--------------------vaccination---------------#
class Patient(models.Model):
    SEXE=[
        ('homme','Homme'),
        ('femme','Femme')
    ]
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    dateNaissance = models.DateField()
    nni = models.BigIntegerField(unique=True)
    sexe = models.CharField(max_length=20, choices=SEXE)

    def __str__(self):
        return f'{self.nom} {self.prenom}'


class Vaccination(models.Model):
    STATUS=[
        ('en_attent','En_Attent'),
        ('certifie','Certifie'),
        ('abondanne','Abondanne')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    center = models.ForeignKey(CentreDeVaccination, on_delete=models.CASCADE)
    dose_number = models.IntegerField(default=0)
    dose_administre = models.IntegerField(default=1)
    date_darnier_dose = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS, default='en_attent')
    qr_code = models.ImageField(upload_to='vaccination_qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR code data
        data = f"Nom: {self.patient.nom} {self.patient.prenom}\nCenter: {self.center.nom}\nMoughataa: {self.center.moughataa}\nType vaccine: {self.vaccine.type.nom}\nVaccine: {self.vaccine.nom}\nTotal doses: {self.dose_number}\nDoses administré: {self.dose_administre}\nDate darnier dose: {self.date_darnier_dose}\nStatus: {self.status}"

        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to field
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.qr_code.save(f"{self.patient.nom}-vaccination-qr-code.png", File(buffer), save=False)

        super(Vaccination, self).save(*args,**kwargs)

    def __str__(self):
        return f'{self.patient.nom}-{self.vaccine.type.nom}-{self.vaccine.nom}'

        
class Vaccin_Dose(models.Model):
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccin = models.ForeignKey(Vaccine, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient.nom} {self.vaccin.nom}'



#-----------------certificat-----------------#
class CertificatVaccination(models.Model):
    id_certificat = models.CharField(max_length=10, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccin = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date_delivration = models.DateField()
    valide = models.BooleanField(default=False)
    # vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='vaccination_qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR code data
        data = f"Certificat Informations\nID certificat: {self.id_certificat}\nDate: {self.date_delivration}\nPersonne vacciné\nNom: {self.patient.nom} {self.patient.prenom}\nDate Naissance: {self.patient.dateNaissance}\nType vaccine: {self.vaccin.type.nom}\nVaccin: {self.vaccin.nom}\nTotal doses: {self.vaccin.total_doses}/{self.vaccin.total_doses}\n"

        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to field
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.qr_code.save(f"{self.patient.nom}-certificat-qr-code.png", File(buffer), save=False)

        super(CertificatVaccination, self).save(*args,**kwargs)


    def __str__(self):
        return f'{self.patient.nom} {self.id_certificat}'

import random

def générer_id_certificat():
    hex_chars = '0123456789ABCDEF'
    return ''.join(random.choice(hex_chars) for _ in range(10))

from datetime import date
def générer_certificat_vaccination(vaccination):
    patient = vaccination.patient
    vaccin = vaccination.vaccine

    if vaccination.dose_administre == vaccin.total_doses:     
        certificat = CertificatVaccination.objects.create(
            id_certificat=générer_id_certificat(),
            patient=patient,
            vaccin=vaccin,
            date_delivration= date.today(),
            valide=True,
            # vaccination=vaccination
        )



#-----------planification-----------#
class ProchaineDose(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccin = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date_vaccination = models.DateField()
    nombre_doses = models.IntegerField(default=2) 

    def __str__(self):
        return f'{self.patient.nom} {self.nombre_doses}'


from datetime import timedelta
def planifier_prochaines_doses(vaccination):
    date_vaccination = vaccination.date_darnier_dose
    nombre_doses_total = Dose.objects.filter(vaccine=vaccination.vaccine)  # Utiliser le champ nombre_doses

    for i in nombre_doses_total:
        print(i.duree)
        prochaine_dose = date_vaccination + timedelta(days=i.duree)
  
        
        notification_date = prochaine_dose - timedelta(days=3)  # Date de la notification, 3 jours avant la dose

        prochaine_dose = ProchaineDose(patient=vaccination.patient, vaccin=vaccination.vaccine, date_vaccination=prochaine_dose, nombre_doses=i.number + 1)
        prochaine_dose.save()

        # planifier_notification_prochaine_dose(vaccination.patient, notification_date)
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
        ('directeur-regional', 'Directeur-Regional'),
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

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

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
    CATEGORIE = (
        ('enfants', 'Enfants'),
        ('jeunes-femmes', 'Jeunes-Femmes'),
        ('jeunes-hommes', 'Jeunes-Hommes'),
        ('veux', 'Veux'),
        ('tout-monde', 'Tout-Monde')
    )
    nom = models.CharField(max_length=50)
    categorie = models.CharField(choices=CATEGORIE, max_length=50)

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
    durée = models.DurationField()
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




@receiver(post_save, sender=StockVaccins)
def create_historiqueStock(sender, instance, created, **kwargs):
    
    if created:
        HistoriqueStock.objects.create(
            typeOperation=instance.typeOperation,
            vaccine=instance.vaccine,
            quantite=instance.quantite,
            dateExpiration=instance.dateExpiration,
            dateOperation=instance.dateOperation,
            centerVaccination=instance.centerVaccination,
            numeroLot = instance.numeroLot
           
        )


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


class Vaccination(models.Model):
    STATUS=[
        ('en_attend','En_Attend'),
        ('validé','Validé'),
        ('abondant','Abondant')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    center = models.ForeignKey(CentreDeVaccination, on_delete=models.CASCADE)
    dose_number = models.IntegerField(default=0)
    dose_administré = models.IntegerField(default=1)
    date_darnier_dose = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS, default='en_attend')
    qr_code = models.ImageField(upload_to='vaccination_qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR code data
        data = f"Nom: {self.patient.nom} {self.patient.prenom}\nCenter: {self.center.nom}\nMoughataa: {self.center.moughataa}\nType vaccine: {self.vaccine.type.nom}\nVaccine: {self.vaccine.nom}\nTotal doses: {self.dose_number}\nDoses administré: {self.dose_administré}\nDate darnier dose: {self.date_darnier_dose}\nStatus: {self.status}"

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

@receiver(pre_save, sender=Vaccination)
def changeStatus(sender, instance,*args, **kwargs):
    if instance.dose_administré == instance.dose_number:
        instance.status = 'validé'
        data = f"Nom: {instance.patient.nom} {instance.patient.prenom}\nCenter: {instance.center.nom}\nMoughataa: {instance.center.moughataa}\nType vaccine: {instance.vaccine.type.nom}\nVaccine: {instance.vaccine.nom}\nTotal doses: {instance.dose_number}\nDoses administré: {instance.dose_administré}\nDate darnier dose: {instance.date_darnier_dose}\nStatus: {instance.status}"

        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to field
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        instance.qr_code.save(f"{instance.patient.nom}-vaccination-qr-code.png", File(buffer), save=False)

        
class Vaccin_Dose(models.Model):
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)
    date_dose = models.DateField()
    numeroDose = models.IntegerField()
    vaccins = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    centre = models.ForeignKey(CentreDeVaccination, on_delete=models.CASCADE)
    numeroLot = models.CharField(max_length=50)







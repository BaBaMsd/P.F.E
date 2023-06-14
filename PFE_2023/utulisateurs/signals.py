
from django.db.models.signals import post_migrate
from datetime import datetime, timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *

@receiver(post_migrate)
def insérer_wilayas(sender, **kwargs):
    if sender.name == 'utulisateurs':  
        wilayas = [
            {'nom': 'Adrar', 'code': '01'},
            {'nom': 'Assaba ', 'code': '02'},
            {'nom': 'Brakna', 'code': '03'},
            {'nom': 'Dakhlet Nouadhibou', 'code': '04'},
            {'nom': 'Gorgol ', 'code': '05'},
            {'nom': 'Guidimaka', 'code': '06'},
            {'nom': 'Hodh Ech Chargui', 'code': '07'},
            {'nom': 'Hodh El Gharbi', 'code': '08'},
            {'nom': 'Inchiri', 'code': '09'},
            {'nom': 'Tagant', 'code': '10'},
            {'nom': 'Tiris Zemmour', 'code': '11'},
            {'nom': 'Trarza ', 'code': '12'},
            {'nom': 'Nouakchott Ouest', 'code': '13'},
            {'nom': 'Nouakchott Nord', 'code': '14'},
            {'nom': 'Nouakchott Sud', 'code': '15'},
        ]

        if not Wilaya.objects.exists():
            # Insérer les wilayas dans la base de données
            for wilaya_data in wilayas:
                Wilaya.objects.create(nom=wilaya_data['nom'], code=wilaya_data['code'])


@receiver(post_save, sender=Vaccination)
def update_patient_status(sender, instance, **kwargs):
    
    vaccin = instance.vaccine
    dose = Dose.objects.get(vaccine=vaccin)
    
    # Vérifier si le patient a reçu deux doses
    for i in dose:
        deadline = instance.date_darnier_dose + timedelta(days=i.durée)
        if datetime.now().date() > deadline:
            instance.status = "abandonne"

        
    instance.save()

    

@receiver(post_save, sender=Vaccination)
def SaveDose(sender, instance, created, **kwargs):  
    if created:
        Vaccin_Dose.objects.create(
            vaccination=instance,
            patient=instance.patient,
            vaccin=instance.vaccine       
        )




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



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(pre_save, sender=Vaccination)
def changeStatus(sender, instance,*args, **kwargs):
    if instance.dose_administre == instance.dose_number:
        instance.status = 'valide'
        data = f"Nom: {instance.patient.nom} {instance.patient.prenom}\nCenter: {instance.center.nom}\nMoughataa: {instance.center.moughataa}\nType vaccine: {instance.vaccine.type.nom}\nVaccine: {instance.vaccine.nom}\nTotal doses: {instance.dose_number}\nDoses administre: {instance.dose_administre}\nDate darnier dose: {instance.date_darnier_dose}\nStatus: {instance.status}"

        générer_certificat_vaccination(instance)

        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to field
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        instance.qr_code.save(f"{instance.patient.nom}-vaccination-qr-code.png", File(buffer), save=False)

        
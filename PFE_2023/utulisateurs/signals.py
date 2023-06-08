# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import HistoriqueStock, StockVaccins , User

# @receiver(post_save, sender=StockVaccins)
# def create_historiqueStock(sender, instance, created, **kwargs):
#     if created:
#         HistoriqueStock.objects.create(
#             typeOperation=instance.typeOperation,
#             vaccine=instance.vaccine,
#             quantite=instance.quantite,
#             dateExpiration=instance.dateExpiration,
#             dateOperation=instance.dateOperation,
#             centerVaccination=instance.centerVaccination,
#             user=kwargs['request'].user
 #       )
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Wilaya

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

        # Vérifier si les wilayas existent déjà dans la base de données
        if not Wilaya.objects.exists():
            # Insérer les wilayas dans la base de données
            for wilaya_data in wilayas:
                Wilaya.objects.create(nom=wilaya_data['nom'], code=wilaya_data['code'])


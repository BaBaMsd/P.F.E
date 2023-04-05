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

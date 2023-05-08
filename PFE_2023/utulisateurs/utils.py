from utulisateurs.models import StockVaccins, User, CentreDeVaccination , AdminCenter
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Sum


def check_stock(request,centre):
    # Récupérer les utilisateurs à qui envoyer des notifications
    utilisateurs = AdminCenter.objects.filter(center=centre, type__in=['gerent-stock', 'admin'])

    # Récupérer les stocks dont la quantité est inférieure à 100 et qui ont le même centre que l'utilisateur connecté
    # stocks = StockVaccins.objects.filter(quantite__lt=100, centerVaccination=centre)
    stock_data = StockVaccins.objects.filter(centerVaccination=centre).select_related('vaccine').values('vaccine__nom').annotate(total_quantite=Sum('quantite'))
    stocks = stock_data.filter(total_quantite__lt=100)
    # for stk in stock_data:
    #     if stock_data.filter(total_quantite__lt=100):
    #         stocks = stocks[stk]
        
    if stocks.exists():
        message = 'Les stocks suivants sont en dessous de 100 :\n\n'
        
        for stock in stocks:
            print(stock)
            message += f"{stock['vaccine__nom']} : {stock['total_quantite']}\n"
            messages.warning(request, f"La quantité de {stock['vaccine__nom']} dans le stock est inférieure à 100.")

        # Envoyer le message à tous les utilisateurs sélectionnés
        recipients = [utilisateur.user.email for utilisateur in utilisateurs]
        send_mail('Notification de stock', message, 'noreply@example.com', recipients, fail_silently=True)
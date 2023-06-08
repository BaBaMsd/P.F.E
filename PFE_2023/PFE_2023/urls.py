from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from utulisateurs.views import *
from utulisateurs.Contrller import auth
from utulisateurs.RestApi import api
urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('patient_rg/', api.register_patient, name='patient_rg'),
    path('login_P/', api.PatientLoginView.as_view(), name='login_P'),
    path('patient_DT/<int:id>/',api.getUserData , name='patient_DT'),

    #template
    path('add_staff/', add_staff, name='add_staff'),
    path('register/', auth.register, name='register'),
    path('', auth.login , name='login'),
    path('profile/', auth.profile, name='profile'),

    path('vaccination_complementaire/<int:id>/', vaccination_complementaire, name='vaccination_complementaire'),
    path('vaccins/', vaccins, name='vaccins'),
    path('vaccination_certificat/', vaccination_certificat, name='vaccination_certificat'),

    path('accueil/<int:id>/', accueil, name='accueil'),
    path('ac/', ac, name='ac'),
    path('centres/', centres, name='centres'),
    path('stock_center/', stock_center, name='stock_center'),
    path('historique_stock/', historique_stock, name='historique_stock'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('add_vaccine/', add_vaccine, name='add_vaccine'),
    path('add_type/', add_type, name='add_type'),
    path('choix_vaccination/', choix_vaccination, name='choix_vaccination'),
    path('add_vaccination/<int:id>/', add_vaccination, name='add_vaccination'),
    path('vaccination_type/', vaccination_type, name='vaccination_type'),
    path("changePassMot/", auth.changePassMot,name = "changePassMot"), 
    path('liste_vaccine/', liste_vaccine, name='liste_vaccine'),
    path('addCenterForm/', addCenterForm, name='addCenterForm'),
    path('stockAddition/', stockAddition , name='stockAddition'),
    path('stockSuppresion/', stockSuppresion , name='stockSuppresion'),
    path('remove_stock/supp/<int:id>/', remove_stock , name='remove_stock'),
    path('vaccines/update/<int:id>/', update_vaccine, name='update_vaccine'),
    path('vaccines/delete/<int:id>/', delete_vaccine, name='supp_vaccine'),
    path('vaccinatiom_type/delete/<int:id>/', delete_vaccination_type, name='supp_type vac'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


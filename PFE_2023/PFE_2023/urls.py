from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from utulisateurs.views import *
from utulisateurs.Contrller import auth
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', auth.register, name='register'),
    path('', auth.login , name='login'),
    path('accueil', accueil, name='accueil'),
    #vaccins
    path('add_vaccine', add_vaccine, name='add_vaccine'),
    path("registerPatient/",auth.PatientRegisterView.as_view(),name = "registerPatient"), 
    path('liste_vaccine/', liste_vaccine, name='liste_vaccine'),
    path('addCenterForm/', addCenterForm, name='addCenterForm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


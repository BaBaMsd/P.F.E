from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from utulisateurs.views import *
from utulisateurs.Contrller import auth
urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_staff/', add_staff, name='add_staff'),
    path('patient_rg/', auth.patient_rg, name='patient_rg'),
    path('register/', auth.register, name='register'),
    path('', auth.login , name='login'),
    path('phone-login/', auth.PhoneLoginView.as_view(), name='phone_login'),
    path('profile/', auth.profile, name='profile'),
    path('vaccination_complementaire/', vaccination_complementaire, name='vaccination_complementaire'),
    path('accueil', accueil, name='accueil'),
    path('centres', centres, name='centres'),
    path('stock_center', stock_center, name='stock_center'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('add_vaccine', add_vaccine, name='add_vaccine'),
    path('add_vaccination', add_vaccination, name='add_vaccination'),
    path("registerPatient/",auth.PatientRegisterView.as_view(),name = "registerPatient"), 
    path('liste_vaccine/', liste_vaccine, name='liste_vaccine'),
    path('addCenterForm/', addCenterForm, name='addCenterForm'),
    path('stockAddition/', stockAddition , name='stockAddition'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


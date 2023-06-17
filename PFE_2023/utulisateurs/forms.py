from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CentreDeVaccination , AdminCenter , Moughataa
from .models import Vaccine, Dose , TypeVaccination , StockVaccins, Profile , Patient , Vaccination
from django.contrib.auth import get_user_model
from django import forms
from utulisateurs.models import User
User = get_user_model()
from datetime import datetime

#<---------------Gestion-de-utilusateurs------------>#

#_formilair_aithentification
class CustomLoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-group mb-3 col-md-12 ',
                'style': 'border-color: #888888;'
            }
        )
    )
    password = forms.CharField(
        label='Mot-de-pass',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control col-md-12',
                'style': 'border-color: #888888;'
            }
        )
    )
#_formilaire_registrations
class CustomUserCreationForm(forms.Form):
    ROLES = (
        ('directeur-regional', 'Directeur-Regional'),
        ('responsable-center', 'Responsable-Center'),
    )
 
    email = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6 my-2'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control col-6 my-2'}))
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={'class':'form-control col-4 my-2'}))

    def save(self):
        # Create a new user
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role=self.cleaned_data['role'],
    )

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Nom', widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6 my-2'}))
    last_name = forms.CharField(label='Prénom',widget=forms.TextInput(attrs={'class':'form-control col-6 my-2'}))
    nni = forms.CharField(label='NNI',widget=forms.TextInput(attrs={'class':'form-control col-6 my-2'}))

    class Meta:
        model = User
        fields = [ 'nni','first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

#<------------------Gestion-des-centers--------------->#

#_ajouter_un_center
from django.core.validators import RegexValidator
phone_regex = RegexValidator(
    regex=r'^(\+2222|\+2223|\+2224|002222|002223|002224|2|3|4)[0-9]{7}$',  # Format international avec ou sans le préfixe '+'
    message="Le numéro de téléphone doit être dans un format valide."
)

nni_regex = RegexValidator(
    #r'^\+?1?\d{9,15}$'
    regex=r'^(\0|\1)[0-9]{9}$',  # Format international avec ou sans le préfixe '+'
    message="Votre NNI doit être dans un format valide."
)
 
class AddCenterForm(forms.Form):
    centre_nom = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-8','style': 'border-color: #888888;'})) 
    centre_moughataa = forms.ChoiceField(choices=[(i.pk, i.nom) for i in Moughataa.objects.all()], widget=forms.Select(attrs={'class':'form-control col-8','style': 'border-color: #888888;'}))
    admin_nom = forms.CharField(max_length=30, widget= forms.TextInput(attrs={'class':'form-control col-8','style': 'border-color: #888888;'}))
    admin_email = forms.EmailField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-8'
    ,'style': 'border-color: #888888;'}))
    phone_number = forms.CharField(
        label="Numéro de téléphone",
        validators=[phone_regex],
         widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-8'
         ,'style': 'border-color: #888888;'}
         ))
    latitude = forms.DecimalField(widget=forms.TextInput(attrs={
        'id': 'lat',
        'class':'form-control input-group mb-3 col-8',
        'style': 'border-color: #888888;'
    }))
    longitude = forms.DecimalField(widget=forms.TextInput(attrs={
        'id': 'lon',
        'class':'form-control input-group mb-3 col-8',
        'style': 'border-color: #888888;'
    }) )

    role = "responsable-center"
    password = "admin2023"

    def save(self):
        # Create a new user
        user = User.objects.create_user(
            first_name=self.cleaned_data['admin_nom'],
            email=self.cleaned_data['admin_email'],
            phone_number=self.cleaned_data['phone_number'],
            password=self.password,
            role=self.role
        )
        # Create a new center
        center = CentreDeVaccination.objects.create(
            nom=self.cleaned_data['centre_nom'],
            moughataa=Moughataa.objects.get(id=self.cleaned_data['centre_moughataa']),
            latitude=self.cleaned_data['latitude'],
            longitude=self.cleaned_data['longitude'],
        )
        # Create a new AdminCenter instance with the user and center foreign keys
        admin_center = AdminCenter.objects.create(user=user, center=center)


#<---------------------vaccins-et-doses---------->#

class VaccineForm(forms.Form):
    nom = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-12','style': 'border-color: #888888;'}))
    type = forms.ChoiceField(label='Type de vaccination',choices=[(i.pk, i.nom) for i in TypeVaccination.objects.all()], widget=forms.Select(attrs={'class':'form-control col-12','style': 'border-color: #888888;'}))
    fabricant = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-12','style': 'border-color: #888888;'}))
    total_doses = forms.IntegerField(min_value=1, widget= forms.TextInput(attrs={'class':'form-control col-12','style': 'border-color: #888888;'}))
    doses_administrées = forms.IntegerField(label='Quantite a administrée',widget= forms.TextInput(attrs={'class':'form-control col-12','style': 'border-color: #888888;'}))
    
    def save(self):
        vaccine = Vaccine.objects.create(
           nom=self.cleaned_data['nom'] ,
           type=TypeVaccination.objects.get(id=self.cleaned_data['type']),
           fabricant=self.cleaned_data['fabricant'],
           total_doses=self.cleaned_data['total_doses'],
           doses_administrées=self.cleaned_data['doses_administrées']
        )

class DoseForm(forms.ModelForm):
    duree = forms.IntegerField(widget=forms.TextInput(attrs={'required': True,'class':'form-control col-12','style': 'border-color: #888888;'}))

    class Meta:
        model = Dose
        fields = ['duree']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['duree'].required = True
        self.fields['duree'].widget.attrs['placeholder'] = 'Durée (in days)'
        self.fields['duree'].widget.attrs['class'] = 'form-control'

        # Add hidden fields for formset
        self.fields['id'].widget = forms.HiddenInput()

DoseFormSet = forms.inlineformset_factory(Vaccine, Dose, form=DoseForm, extra=0, min_num=1)

#<------------------------------Gestion-stock--------------------------->#

class StockForm(forms.Form):
    OPERATION_CHOICES = [
        ('AJOUTER', 'Addition'),
        ('SUPRIMER', 'Suppresion'),
    ]
    typeOperation = 'Addition'
    # typeOperation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.Select(attrs={'class':'form-control col-4 my-2'}))
    vaccine = forms.ChoiceField(choices=[(i.pk, i.nom) for i in Vaccine.objects.all()], widget=forms.Select(attrs={'class':'form-control col-md-12',
                'style': 'border-color: #888888; '}))
    quantite = forms.IntegerField( widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-md-12',
                'style': 'border-color: #888888;'}))
    dateExpiration = forms.DateField(widget= forms.DateInput(attrs={
        'class':'datepicker form-control col-md-12',
                'style': 'border-color: #888888;',
        'type': 'date'}))
    numeroLot = forms.CharField(label= "Numéro de Lot", widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-md-12',
                'style': 'border-color: #888888;'}))

    
    def save(self, commit=True, request=None):
        user= request.user if request else None
        center = AdminCenter.objects.get(user=user)
        ligne = StockVaccins.objects.create(
            typeOperation=self.typeOperation,
            vaccine=Vaccine.objects.get(id=self.cleaned_data['vaccine']),
            centerVaccination=center.center,
            quantite=self.cleaned_data['quantite'],
            numeroLot=self.cleaned_data['numeroLot'],
            dateExpiration=self.cleaned_data['dateExpiration'],
        )
#---------------------vaccination----------------#
from datetime import date
#--------------staff------------------#
class Add_staff(forms.Form):
    ROLES = (
        ('professionnel','Professionnel'),
        ('gerent-stock','Gerent-Stock'),
    )
    phone_number = forms.CharField(
        label="Numéro de téléphone",
        validators=[phone_regex],
         widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-md-12',
                'style': 'border-color: #888888;'}
         ))
    email = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-md-12',
                'style': 'border-color: #888888;'}))
    password = 'emp2023'
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={'class':'form-control col-col-md-12',
                'style': 'border-color: #888888;'}))

    def save(self, commit=True, request=None):
        user= request.user if request else None
        center = AdminCenter.objects.get(user=user)
        # Create a new user
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number'],
            password=self.password,
            role=self.cleaned_data['role'],
        )

        admin_center = AdminCenter.objects.create(user=user, center=center.center)


class ID_crf(forms.Form):
    Id = forms.CharField(label='ID Certificat',widget=forms.TextInput(attrs={'class': 'form-control col-md-12',
                'style': 'border-color: #888888;','name':'nni'}))

    class Meta:
        model = CentreDeVaccination
        fields = [ 'id_certificat']

class Vac_type(forms.Form):
    SEXE=[
        ('homme','Homme'),
        ('femme','Femme'),
        ('tous', 'Tous...')
    ] 
    nom = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    description = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    sexe_cible = forms.ChoiceField(choices=SEXE, widget=forms.Select(attrs={'class':'form-control col-3 my-2'}))
    age_minimum = forms.IntegerField( widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-3'}))
    age_maximum = forms.IntegerField( widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-3'}))
    def save(self):
        tp = TypeVaccination.objects.create(
            nom = self.cleaned_data['nom'],
            sexe_cible = self.cleaned_data['sexe_cible'],
            description=self.cleaned_data['description'],
            age_minimum=self.cleaned_data['age_minimum'],
            age_maximum=self.cleaned_data['age_maximum']
        )
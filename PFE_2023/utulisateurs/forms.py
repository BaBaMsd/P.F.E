from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CentreDeVaccination , AdminCenter , Moughataa
from .models import Vaccine, Dose , TypeVaccination , StockVaccins, Profile
from django.contrib.auth import get_user_model
from django import forms
from utulisateurs.models import User
User = get_user_model()

#<---------------Gestion-de-utilusateurs------------>#

#_formilair_aithentification
class CustomLoginForm(forms.Form):
    email = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6 my-2'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control col-6 my-2'}))

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


    class Meta:
        model = User
        fields = [ 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

#<------------------Gestion-des-centers--------------->#

#_ajouter_un_center
class AddCenterForm(forms.Form):
    nom = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    moughataa = forms.ChoiceField(choices=[(i.pk, i.nom) for i in Moughataa.objects.all()], widget=forms.Select(attrs={'class':'form-control col-6 '}))
    admin_nom = forms.CharField(max_length=30, widget= forms.TextInput(attrs={'class':'form-control col-6'}))
    admin_email = forms.EmailField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    latitude = forms.DecimalField(widget=forms.TextInput(attrs={
        'id': 'lat',
        'class':'form-control input-group mb-3 col-6'
    }))
    longitude = forms.DecimalField(widget=forms.TextInput(attrs={
        'id': 'lon',
        'class':'form-control input-group mb-3 col-6'
    }) )

    role = "responsable-center"
    password = "admin2023"

    def save(self):
        # Create a new user
        user = User.objects.create_user(
            first_name=self.cleaned_data['admin_nom'],
            email=self.cleaned_data['admin_email'],
            password=self.password,
            role=self.role
        )
        # Create a new center
        center = CentreDeVaccination.objects.create(
            nom=self.cleaned_data['nom'],
            moughataa=Moughataa.objects.get(id=self.cleaned_data['moughataa']),
            latitude=self.cleaned_data['latitude'],
            longitude=self.cleaned_data['longitude'],
        )
        # Create a new AdminCenter instance with the user and center foreign keys
        admin_center = AdminCenter.objects.create(user=user, center=center)


#<---------------------vaccins-et-doses---------->#

class VaccineForm(forms.Form):
    nom = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    type = forms.ChoiceField(choices=[(i.pk, i.nom) for i in TypeVaccination.objects.all()], widget=forms.Select(attrs={'class':'form-control col-6 '}))
    fabricant = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    total_doses = forms.IntegerField(min_value=1, widget= forms.TextInput(attrs={'class':'form-control col-6'}))
    doses_administrées = forms.IntegerField(widget= forms.TextInput(attrs={'class':'form-control col-6'}))
    
    def save(self):
        vaccine = Vaccine.objects.create(
           nom=self.cleaned_data['nom'] ,
           type=TypeVaccination.objects.get(id=self.cleaned_data['type']),
           fabricant=self.cleaned_data['fabricant'],
           total_doses=self.cleaned_data['total_doses'],
           doses_administrées=self.cleaned_data['doses_administrées']
        )

class DoseForm(forms.ModelForm):
    durée = forms.CharField(widget=forms.TextInput(attrs={'required': True,'class':'form-control col-6'}))

    class Meta:
        model = Dose
        fields = ['durée']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['durée'].required = True
        self.fields['durée'].widget.attrs['placeholder'] = 'Durée (in days)'
        self.fields['durée'].widget.attrs['class'] = 'form-control'

        # Add hidden fields for formset
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['DELETE'].widget = forms.HiddenInput()

DoseFormSet = forms.inlineformset_factory(Vaccine, Dose, form=DoseForm, extra=0, min_num=1)

#<------------------------------Gestion-stock--------------------------->#

class StockForm(forms.Form):
    OPERATION_CHOICES = [
        ('AJOUTER', 'Addition'),
        ('SUPRIMER', 'Suppresion'),
    ]
    typeOperation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.Select(attrs={'class':'form-control col-4 my-2'}))
    vaccine = forms.ChoiceField(choices=[(i.pk, i.nom) for i in Vaccine.objects.all()], widget=forms.Select(attrs={'class':'form-control col-6 '}))
    quantite = forms.IntegerField( widget= forms.TextInput(attrs={'class':'form-control input-group mb-3 col-6'}))
    dateExpiration = forms.DateField(widget= forms.DateInput(attrs={
        'class':'datepicker form-control col-6',
        'type': 'date'}))
   
    
    def save(self, commit=True, request=None):
        user= request.user if request else None
        center = AdminCenter.objects.get(user=user)
        ligne = StockVaccins.objects.create(
            typeOperation=self.cleaned_data['typeOperation'] ,
            vaccine=Vaccine.objects.get(id=self.cleaned_data['vaccine']),
            #vaccine=self.cleaned_data['vaccine'],
            centerVaccination=center.center,
            #centerVaccination=CentreDeVaccination.objects.get(id=self.cleaned_data['centerVaccination']),
            quantite=self.cleaned_data['quantite'],
            dateExpiration=self.cleaned_data['dateExpiration'],
        )


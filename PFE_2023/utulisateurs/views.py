from django.shortcuts import render
from .EmailBackend import *
from .models import *
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import  login as Login_process, logout 
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

@login_required
#@user_passes_test(lambda u: u.role == 'directeur-regional')
def addCenterForm(request):
    if request.method == 'POST':
        form = AddCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')

    else:
        form = AddCenterForm()

    return render(request, 'addCenterForm.html', {'form': form})
from django.db.models import Count
from datetime import date
def accueil(request):
    if request.user.role == 'responsable-center' or request.user.role == 'gerent-stock' or request.user.role == 'professionnel':
        centre = AdminCenter.objects.get(user=request.user)
        vaccinations = Vaccination.objects.filter(center=centre.center)
    else:
        vaccinations = Vaccination.objects.all()

    # Compter les vaccinations par état
    status_counts = {}
    for vaccination in vaccinations:
        if vaccination.status in status_counts:
            status_counts[vaccination.status] += 1
        else:
            status_counts[vaccination.status] = 1
    # compte le vaccination par centres
    centre_counts = {}
    for vaccination in vaccinations:
        if vaccination.center in centre_counts:
            centre_counts[vaccination.center] += 1
        else:
            centre_counts[vaccination.center] = 1

    # Compter les vaccinations par type de vaccin
    vaccine_counts = {}
    for vaccination in vaccinations:
        if vaccination.vaccine.nom in vaccine_counts:
            vaccine_counts[vaccination.vaccine.nom] += 1
        else:
            vaccine_counts[vaccination.vaccine.nom] = 1

    # Compter les vaccinations par moughataa
    vaccinations_by_moughataa = {}
    for vaccination in vaccinations:
        if vaccination.center.moughataa in vaccinations_by_moughataa:
            vaccinations_by_moughataa[vaccination.center.moughataa] += 1
        else:
            vaccinations_by_moughataa[vaccination.center.moughataa] = 1

    # Compter les vaccinations par wilaya
    wilaya_counts = {}
    for vaccination in vaccinations:
        if vaccination.center.moughataa.wilaya in wilaya_counts:
            wilaya_counts[vaccination.center.moughataa.wilaya] += 1
        else:
            wilaya_counts[vaccination.center.moughataa.wilaya] = 1
     # Compter les vaccinations par âge
    age_counts = {
        '1-18': 0,
        '18-30': 0,
        '30-50': 0,
        '50+': 0
    }
    today = date.today()
    for vaccination in vaccinations:
        age = today.year - vaccination.patient.dateNaissance.year
        if today.month < vaccination.patient.dateNaissance.month or \
                (today.month == vaccination.patient.dateNaissance.month and today.day < vaccination.patient.dateNaissance.day):
            age -= 1
        if age <= 18:
            age_counts['1-18'] += 1
        elif age <= 30:
            age_counts['18-30'] += 1
        elif age <= 50:
            age_counts['30-50'] += 1
        else:
            age_counts['50+'] += 1

    patients = Patient.objects.all()
    total_patient = patients.count()
    sex_count1 = patients.values('sexe').annotate(count=Count('sexe'))
    sex_percentages = {}
    for sex_count in sex_count1:
        sex_percentages[sex_count['sexe']] = round(sex_count['count'] / total_patient * 100)

    sex_counts = {}
    sex_labels = ['femme', 'homme']
    for label in sex_labels:
        sex_counts[label] = vaccinations.filter(patient__sexe=label).count()
    

    # Créer des listes pour les données des graphiques
    status_labels = list(status_counts.keys())
    status_values = list(status_counts.values())
    vaccine_labels = list(vaccine_counts.keys())
    vaccine_values = list(vaccine_counts.values())

    # Passer les données aux templates
    context = {
        'status_counts': status_counts,
        'vaccine_counts': vaccine_counts,
        'vaccinations_by_moughataa': vaccinations_by_moughataa,
        'wilaya_counts': wilaya_counts,
        'status_labels': status_labels,
        'status_values': status_values,
        'vaccine_labels': vaccine_labels,
        'vaccine_values': vaccine_values,
        'centre_counts': centre_counts,
        'age_counts': age_counts,
        'sex_counts': sex_counts,
        'sex_percentages': sex_percentages, 
        'total_patient': total_patient
    }

    return render(request, 'accueil.html',context)

def centres(request):
    centres = CentreDeVaccination.objects.all()
    return render(request, 'centres.html',{'centres': centres})

@login_required
def liste_vaccine(request):

    vaccine = Vaccine.objects.all()

    return render(request, 'liste_vaccine.html', {'vaccine': vaccine})

#<--------------------vaccinsDose----------->

from django.shortcuts import render, redirect
from .forms import VaccineForm , DoseForm, DoseFormSet 
from .models import Dose, Vaccine
from .models import Vaccine, Dose

@login_required
def add_vaccine(request):
    DoseFormSet = forms.inlineformset_factory(Vaccine, Dose, form=DoseForm, extra=0, min_num=1)
    if request.method == 'POST':
        vaccine_form = VaccineForm(request.POST)
        formset = DoseFormSet(request.POST)
        if vaccine_form.is_valid():

            vaccine = vaccine_form.save()
            doses_number = vaccine_form.cleaned_data['total_doses']

            DoseFormSet = forms.inlineformset_factory(Vaccine, Dose, form=DoseForm, extra=doses_number - 2, min_num=1)
            formset = DoseFormSet()
            context = {
                'formset': formset
            }
            return render(request, 'add_vaccine.html', context)
        if formset.is_valid():       
            doses = formset.save(commit=False)
            i = 0
            for dose in doses:
                i = i + 1
                dose.vaccine = Vaccine.objects.latest('id')
                dose.number = i
                dose.save()
            return redirect('accueil')
    else:
        vaccine_form = VaccineForm()

    context = {
        'vaccine_form': vaccine_form,
        #'formset': formset,
    }
    return render(request, 'add_vaccine.html', context)

def delete_vaccine(request, id):
    vaccine = Vaccine.objects.get(id=id)
    vaccine.delete()
    messages.success(request, 'La vaccination a été supprimée avec succès')
    return redirect(reverse('liste_vaccine'))
    
def update_vaccine(request, id):
    vaccine = get_object_or_404(Vaccine, id=id) 
    form = VaccineForm(request.POST or None, instance=vaccine) 
    if form.is_valid(): 
        form.save()
        messages.success(request, 'La vaccination a été modifiée avec succès')
        return redirect(reverse('vaccines_list'))
    context = {'form': form}
    return render(request, 'vaccine_mod_form.html', context)

#<----------------stock--------------------->#
@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'gerent-stock'])
def stockAddition(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save(commit=False,request=request)
            return redirect('/')
    else:
        form = StockForm()

    return render(request, 'stock/stockage.html', {'stockf': form})

from django.shortcuts import render
import matplotlib.pyplot as plt
from django.db.models import Sum

@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'gerent-stock'])
def stock_center(request):
    centerAdmin = AdminCenter.objects.get(user=request.user)
    center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)

    stock_data = StockVaccins.objects.filter(centerVaccination=center).values('vaccine').annotate(total_quantite=Sum('quantite'))
    #stock_data = StockVaccins.objects.all()

    context = {"stock_data": stock_data,'center': center}

    # Rendre le template avec le contexte
    return render(request, "stock/stock_donnest.html", context)

@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'professionnel'])
def add_vaccination(request):
    
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccine1 = form.cleaned_data['vaccine']
            v = Vaccine.objects.get(id=vaccine1)
            print(v.doses_administrées)
            admin = AdminCenter.objects.get(user=request.user)
            center=admin.center
            stockage = StockVaccins.objects.filter(vaccine=vaccine1,
            centerVaccination=center,
            dateExpiration__gte=datetime.today(),
            quantite__gte=v.doses_administrées
            ).order_by('dateExpiration').first()
            if stockage:
                stockage.quantite = stockage.quantite - v.doses_administrées
                stockage.save()
                form.save(commit=False,request=request)
                certificat = Vaccination.objects.latest('id')
                context = {
                    'cr': certificat
                }
                return render(request, 'vaccination/certificat.html', context)
            else:
                messages.error(request, 'Quantité insuffisante en stock pour vacciner.')
    else:
        form = VaccinationForm()
    return render(request, 'vaccination/vaccinationForm.html', {'form':form})


def vaccination_complementaire(request):
    if request.method == 'POST':
        form = Complemantaire_V(request.POST)
        if form.is_valid():
            nni = form.cleaned_data['nni']
            patien = Patient.objects.get(nni=nni)
            certificats = Vaccination.objects.get(patient=patien)
            admin = AdminCenter.objects.get(user=request.user)
            center=admin.center
            certificats.dose_administré += 1
            certificats.date_darnier_dose = datetime.today()
            certificats.center=center
            certificats.save()
            context = {
                    'cr': certificats
                }
            return render(request, 'vaccination/certificat.html', context)
        else:
            return redirect('vaccination_complementaire')
    else:
        form = Complemantaire_V()
        return render(request, 'vaccination/vaccination_C.html', {'form':form})



#--------------------add_staff-----------------#
@login_required
@user_passes_test(lambda u: u.role == 'responsable-center')
def add_staff(request):
    if request.method == 'POST':
        form = Add_staff(request.POST)
        if form.is_valid():
            form.save(commit=False,request=request)
            return redirect('add_staff')
    else:
        form = Add_staff()

    return render(request, 'registration/add_staff.html', {'form': form})

#======------------tst-------======$#
@login_required
# @user_passes_test(lambda u: u.role == '')
def vaccination_type(request):

    type_vaccination = TypeVaccination.objects.all()

    return render(request, 'vaccination_type.html', {'type_vaccination': type_vaccination})
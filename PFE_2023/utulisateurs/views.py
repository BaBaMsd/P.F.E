from django.shortcuts import render
from .EmailBackend import *
from .models import *
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.db.models import Sum
from utulisateurs.utils import check_stock
from django.db.models import Count
from datetime import date
from django.shortcuts import render, redirect
from .forms import VaccineForm , DoseForm 
from .models import Dose, Vaccine

@login_required
#@user_passes_test(lambda u: u.role == 'directeur-regional')
def addCenterForm(request):
    if request.method == 'POST':
        form = AddCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addCenterForm')

    else:
        form = AddCenterForm()

    return render(request, 'addCenterForm.html', {'form': form})
@login_required
def ac(request):
    type_vaccination = TypeVaccination.objects.all()
    idtp = type_vaccination[0].id   
    
    return redirect('accueil', id=idtp)

def accueil(request, id):
    type_v = TypeVaccination.objects.get(id=id)
    if request.user.role == 'responsable-center' or request.user.role == 'gerent-stock' or request.user.role == 'professionnel':
        centre = AdminCenter.objects.get(user=request.user)
        vaccinations = Vaccination.objects.filter(center=centre.center, vaccine__type=type_v)
    else:
        vaccinations = Vaccination.objects.filter(vaccine__type=type_v)

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
    sex_labels = ['Femme', 'Homme']
    for label in sex_labels:
        sex_counts[label] = vaccinations.filter(patient__sexe=label).count()
    

    # Créer des listes pour les données des graphiques
    status_labels = list(status_counts.keys())
    status_values = list(status_counts.values())
    vaccine_labels = list(vaccine_counts.keys())
    vaccine_values = list(vaccine_counts.values())
    wilaya_labels = list(wilaya_counts.keys())
    wilaya_values = list(wilaya_counts.values())

    type_vs = TypeVaccination.objects.all()

    # Passer les données aux templates
    context = {
        'status_counts': status_counts,
        'vaccine_counts': vaccine_counts,
        'vaccinations_by_moughataa': vaccinations_by_moughataa,
        'wilaya_counts': wilaya_counts,
        'status_labels': status_labels,
        'status_values': status_values,
        'wilaya_labels': wilaya_labels,
        'wilaya_values': wilaya_values,
        'vaccine_labels': vaccine_labels,
        'vaccine_values': vaccine_values,
        'centre_counts': centre_counts,
        'age_counts': age_counts,
        'sex_counts': sex_counts,
        'sex_percentages': sex_percentages, 
        'total_patient': total_patient,
        'type_v': type_v,
        'type_vs': type_vs,
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



@login_required
def add_vaccine(request):
    DoseFormSet = forms.inlineformset_factory(Vaccine, Dose, form=DoseForm, extra=0, min_num=1)
    if request.method == 'POST':
        vaccine_form = VaccineForm(request.POST)
        formset = DoseFormSet(request.POST)
        if vaccine_form.is_valid():

            vaccine = vaccine_form.save()
            doses_number = vaccine_form.cleaned_data['total_doses']
            if doses_number == 1:
                messages.success(request, 'La vaccin a bien ajouter')
                return redirect('add_vaccine')

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
            messages.success(request, 'La vaccin a bien ajouter')
            return redirect('add_vaccine')
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
            messages.success(request, 'Quantite est bien ajouter dans le stock!')
            return redirect('stockAddition')
    else:
        form = StockForm()

    return render(request, 'stock/stockage.html', {'stockf': form})

@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'gerent-stock'])
def historique_stock(request):
    ad = AdminCenter.objects.get(user=request.user)
    histoir=HistoriqueStock.objects.filter(centerVaccination=ad.center).order_by('-id')

    contex = {
        'histoir': histoir
    }

    return render(request, 'histoir.html', contex)



@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'gerent-stock'])
def stockSuppresion(request):
    if request.method == 'POST':
        vaccine = Vaccine.objects.get(nom=request.POST['vaccine'])
        quantite_a_supprimer = int(request.POST['quantite'])
        stock = StockVaccins.objects.filter(vaccine=vaccine)

        total_disponible = sum([s.quantite for s in stock])
        if quantite_a_supprimer > total_disponible:
            # Si la quantité à retirer est supérieure à la quantité disponible, affiche une erreur
            messages.error(request, "La quantité à retirer est supérieure à la quantité disponible dans le stock.")
            return redirect('stockSuppresion')
         # Retire la quantité de doses de vaccin du stock
        for s in stock:
            if s.quantite >= quantite_a_supprimer:
                s.quantite -= quantite_a_supprimer
                s.save()
                break
            else:
                quantite_a_supprimer -= s.quantite
                s.quantite = 0
                s.save()
        messages.success(request, 'L\'operation effectuer avec succée ')
        centerAdmin = AdminCenter.objects.get(user=request.user)
        center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)
        histoir = HistoriqueStock.objects.create(
            typeOperation='Suppresion',
            quantite=quantite_a_supprimer,
            dateExpiration = date.today(),
            vaccine = vaccine,
            centerVaccination=center
        )
        # Redirige vers la page de détail de la vaccination
        return redirect('stockSuppresion')

    centerAdmin = AdminCenter.objects.get(user=request.user)
    center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)
    stock_data = StockVaccins.objects.filter(centerVaccination=center).distinct('vaccine')


    return render(request, 'stock/stockSuppresion.html', {'stock_data': stock_data})

@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'gerent-stock'])
def stock_center(request):
    centerAdmin = AdminCenter.objects.get(user=request.user)
    center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)

    check_stock(request,centre=center)
    stock_data = StockVaccins.objects.filter(centerVaccination=center).select_related('vaccine').values('vaccine__nom').annotate(total_quantite=Sum('quantite'))
    



    context = {"stock_data": stock_data,'center': center}

    # Rendre le template avec le contexte
    return render(request, "stock/stock_donnest.html", context)

import random

def générer_id_certificat():
    hex_chars = '0123456789ABCDEF'
    return ''.join(random.choice(hex_chars) for _ in range(10))


@login_required
@user_passes_test(lambda u: u.role in ['responsable-center', 'professionnel'])
def add_vaccination(request):
    
    if request.method == 'POST':
        centerAdmin = AdminCenter.objects.get(user=request.user)
        center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)
        vaccine = Vaccine.objects.get(id=request.POST['vaccine'])
        if Vaccination.objects.filter(patient__nni=request.POST['nni'],vaccine__type=vaccine.type).exists():
            print('exist')
            messages.error(request, "Ce patient a déja pris cette vaccination!")
            return redirect('add_vaccination')
        elif Patient.objects.filter(nni=request.POST['nni']).exists():
            patient_av = Patient.objects.get(nni=request.POST['nni'])
            vaccination = Vaccination()
            vaccination.patient = patient_av
            vaccination.vaccine=vaccine
            vaccination.dose_number =vaccine.total_doses
            vaccination.center = center     
            vaccination.date_darnier_dose = datetime.now().strftime('%Y-%m-%d')
        
            stockage = StockVaccins.objects.filter(vaccine=vaccine,
            centerVaccination=center,
            dateExpiration__gte=datetime.today(),
            quantite__gte=vaccine.doses_administrées 
            ).order_by('dateExpiration').first()
            if stockage:
                stockage.quantite = stockage.quantite - vaccine.doses_administrées
                stockage.save()
                vaccination.save()
                certificat = Vaccination.objects.get(patient=patient)
                if CertificatVaccination.objects.filter(patient=certificat.patient).exists():
                    id_certificat =  CertificatVaccination.objects.get(patient=certificat.patient)
                    context = {
                        'cr': certificat,
                        'id_certificat': id_certificat
                    }
                else:
                    context = {
                        'cr': certificat
                    }
                return render(request, 'vaccination/certificat.html', context)
            else:
                messages.error(request, 'Quantité insuffisante en stock pour vacciner.')
        else:
                # Création de l'objet Patient
            patient = Patient()
            patient.nom = request.POST['nom']
            patient.prenom = request.POST['prenom']
            patient.nni = request.POST['nni']
            patient.sexe = request.POST['sexe']
            patient.dateNaissance = request.POST['dateNaissence']
            

            # Création de l'objet Vaccination
            vaccination_p = Vaccination()
            vaccination_p.vaccine = vaccine
            vaccination_p.dose_number = vaccine.total_doses
            vaccination_p.center = center
            vaccination_p.date_dernier_dose = datetime.now().strftime('%Y-%m-%d')
            

            # Mise à jour de l'objet StockVaccins
            stockage = StockVaccins.objects.filter(
                vaccine=vaccine,
                centerVaccination=center,
                dateExpiration__gte=datetime.today(),
                quantite__gte=vaccine.doses_administrées
            ).order_by('dateExpiration').first()

            if stockage:
                stockage.quantite = stockage.quantite - vaccine.doses_administrées
                stockage.save()
                patient.save()
                vaccination_p.patient = patient
                vaccination_p.save()
                certificat = Vaccination.objects.get(patient=patient)
                if CertificatVaccination.objects.filter(patient=certificat.patient).exists():
                    id_certificat =  CertificatVaccination.objects.get(patient=certificat.patient)
                    context = {
                        'cr': certificat,
                        'id_certificat': id_certificat
                    }
                else:
                    context = {
                        'cr': certificat
                    }
                return render(request, 'vaccination/certificat.html', context)
            else:
                messages.error(request, 'Quantité insuffisante en stock pour vacciner.')
     
    centerAdmin = AdminCenter.objects.get(user=request.user)
    center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)
    stock_data = StockVaccins.objects.filter(centerVaccination=center).distinct('vaccine')

    return render(request, 'vaccination/vaccinationForm.html', {'stock_data':stock_data})

def vaccination_certificat(request):
    if request.method == 'POST':
        form = ID_crf(request.POST)
        if form.is_valid():
            ID = form.cleaned_data['Id']
            if CertificatVaccination.objects.filter(id_certificat=ID).exists():
                id_certificat =  CertificatVaccination.objects.get(id_certificat=ID)
                Dose = Vaccin_Dose.objects.filter(patient=id_certificat.patient,vaccin=id_certificat.vaccin)
                context = {
                    'Dose':Dose,
                    'id_certificat': id_certificat
                }
                return render(request, 'vaccination/CRF.html', context)
            else:
                messages.error(request,'N\'exist pas ')
                return redirect('vaccination_certificat')
        else:
            return redirect('vaccination_certificat')
    else:
        form = ID_crf()
        return render(request, 'vaccination/vaccination_certificat.html', {'form':form})


def vaccination_complementaire(request):
    if request.method == 'POST':
        form = Complemantaire_V(request.POST)
        if form.is_valid():
            nni = form.cleaned_data['nni']
            if Patient.objects.filter(nni=nni).exists(): 
                patien = Patient.objects.get(nni=nni)   
                certificats = Vaccination.objects.get(patient=patien)
                if Dose.objects.filter(vaccine=certificats.vaccine).exists:
                    dure = Dose.objects.filter(vaccine=certificats.vaccine)
                    for i in dure:
                        if i.number == certificats.dose_administré and i.durée > certificats.date_darnier_dose - date.today():
                            messages.error(request, 'Imposible de prendre ce dose avant que le duree est fini')
                            return redirect('vaccination_complementaire')
                    admin = AdminCenter.objects.get(user=request.user)
                    center=admin.center
                    certificats.dose_administré += 1    
                    certificats.date_darnier_dose = datetime.today()
                    certificats.center=center
                    certificats.save()
                    dose = Vaccin_Dose()
                    dose.vaccination=certificats
                    dose.patient=certificats.patient
                    dose.vaccin=certificats.vaccine
                    dose.save()               
                    id_certificat =  CertificatVaccination.objects.get(patient=certificats.patient)
                    context = {
                                'cr': certificats,
                                'id_certificat': id_certificat
                    }
                    return render(request, 'vaccination/certificat.html', context)
                            
                else:
                    messages.error(request, 'Ce vaccin a un seul dose ok!')
                    return redirect('vaccination_complementaire')
                
            else:
                messages.error(request, 'Ce NNI ne corespond pas a un patient')
                return redirect('vaccination_complementaire')
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

from operator import attrgetter

def sort_vaccination_stock(vaccine):
    # Trier le stock pour cette vaccination en fonction de la date d'expiration et de la date d'ajout
    sorted_stock = sorted(StockVaccins.vaccine_set.all(), key=attrgetter('dateExpiration', 'dateOperation'))
    return sorted_stock

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse


def remove_stock(request, id):
    vaccine = get_object_or_404(Vaccine, pk=id)
    stock = sort_vaccination_stock(vaccine) # Trie le stock de vaccination
    quantite_a_supprimer = int(request.POST['quantite'])
    
    # Vérifie si la quantité à retirer est inférieure ou égale à la quantité disponible
    total_disponible = sum([s.quantite for s in stock])
    if quantite_a_supprimer > total_disponible:
        # Si la quantité à retirer est supérieure à la quantité disponible, affiche une erreur
        error_message = "La quantité à retirer est supérieure à la quantité disponible."
        return redirect('/')
       # return render(request, 'myapp/remove_stock.html', {'vaccination': vaccine, 'error_message': error_message})
    
    # Retire la quantité de doses de vaccin du stock
    for s in stock:
        if s.quantite >= quantite_a_supprimer:
            s.quantite -= quantite_a_supprimer
            s.save()
            break
        else:
            quantite_a_supprimer -= s.quantite
            s.quantite = 0
            s.save()
    messages.success(request, 'Opp ok')
    # Redirige vers la page de détail de la vaccination
    return HttpResponseRedirect('/')
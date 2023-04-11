from django.shortcuts import render
from .EmailBackend import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import  login as Login_process, logout 
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

@login_required
@user_passes_test(lambda u: u.role == 'directeur-regional')
def addCenterForm(request):
    if request.method == 'POST':
        form = AddCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = AddCenterForm()

    return render(request, 'addCenterForm.html', {'form': form})

def accueil(request):

    return render(request, 'accueil.html')

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

#<----------------stock--------------------->#
@login_required
@user_passes_test(lambda u: u.role == 'responsable-center')
def stockAddition(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save(commit=False,request=request)
            return redirect('login')
    else:
        form = StockForm()

    return render(request, 'stock/stockage.html', {'stockf': form})

from django.shortcuts import render
import matplotlib.pyplot as plt
from django.db.models import Sum

@login_required
@user_passes_test(lambda u: u.role == 'responsable-center')
def stock_center(request):
    centerAdmin = AdminCenter.objects.get(user=request.user)
    center = CentreDeVaccination.objects.get(id=centerAdmin.center.id)

    stock_data = StockVaccins.objects.filter(centerVaccination=center).values('vaccine').annotate(total_quantite=Sum('quantite'))
    #stock_data = StockVaccins.objects.all()

    context = {"stock_data": stock_data,'center': center}

    # Rendre le template avec le contexte
    return render(request, "stock/stock_donnest.html", context)

   
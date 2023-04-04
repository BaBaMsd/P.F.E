from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics
from .serializers import  PatientSerializer
from .EmailBackend import *
from .models import *
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import  login as Login_process, logout 
from django.contrib import messages
from .forms import *

# Create your views here.


'''class PatientRegisterView(generics.CreateAPIView):   
    model = get_user_model()
    serializer_class = PatientSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status= Response.status_code)




def login(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

        if user is not None:
            Login_process(request, user)
            return redirect('accueil')
        else:
            messages.error(request, 'email ou mot pass invalid ')
            print("po")
            return redirect('login')
    form = CustomLoginForm()
    return render(request, 'registration/login.html' , {'form' : form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
'''
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

def liste_vaccine(request):

    vaccine = Vaccine.objects.all()

    return render(request, 'liste_vaccine.html', {'vaccine': vaccine})

#<--------------------vaccinsDose----------->

from django.shortcuts import render, redirect
from .forms import VaccineForm , DoseForm, DoseFormSet 
from .models import Dose, Vaccine
from .models import Vaccine, Dose

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

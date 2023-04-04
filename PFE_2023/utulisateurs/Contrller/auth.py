from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics
from utulisateurs.serializers import  PatientSerializer
from utulisateurs.EmailBackend import *
from utulisateurs.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import  login as Login_process, logout 
from django.contrib import messages
from utulisateurs.forms import *

class PatientRegisterView(generics.CreateAPIView):   
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

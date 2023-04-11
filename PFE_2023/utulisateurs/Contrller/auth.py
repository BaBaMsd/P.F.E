from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics
from utulisateurs.serializers import  PatientSerializer
from utulisateurs.EmailBackend import EmailBackend
from utulisateurs.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import  login as Login_process, logout 
from django.contrib import messages
from utulisateurs.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

class PatientRegisterView(generics.CreateAPIView):   
    model = get_user_model()
    serializer_class = PatientSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status= Response.status_code)



#_authentifications par email

def login(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))

        if user is not None:
            Login_process(request, user)
            return redirect('accueil')
        else:
            messages.error(request, 'email ou mot pass invalid ')
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


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profil.html', context)
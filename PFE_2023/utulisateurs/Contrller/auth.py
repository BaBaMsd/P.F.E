from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics
from utulisateurs.serializers import  PatientSerializer, PhoneLoginSerializer 
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


#--------------test--------------------#
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utulisateurs.serializers import PatientRGS
from utulisateurs.models import User

@api_view(['GET','POST'])
def patient_rg(request):
    nni=request.POST.get('nni')
    try:
        patien = Patient.objects.get(nni=nni)
    except Patient.DoesNotExist:
        return Response({'error':'NNI does not exist in the database'})


    if request.method == 'POST':
        request.data['nni']= patien.nni #_Ajouter
        serializer = PatientRGS(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Compte creer'})
        else:
            Response(serializer.errors)
            return Response({'nni':user.nni,'email':user.email})

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
            messages.success(request, f'Votre profile est modifier ')
            return redirect('profile')
        else:
            messages.error(request, f'il y a une erreur ')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profil.html', context)

#@-------------------
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class PhoneLoginView(ObtainAuthToken):
    serializer_class = PhoneLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
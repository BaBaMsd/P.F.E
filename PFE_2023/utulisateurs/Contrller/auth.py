from django.shortcuts import render
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

#_authentifications par email

def login(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))

        if user is not None:
            Login_process(request, user)
            if user.role == 'gerent-stock':
                return redirect('stock_center')
            if user.role == 'professionnel':
                return redirect('choix_vaccination')
            return redirect('ac')
        else:
            messages.error(request, 'Email ou mot pass invalid ')
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

    #-----------chang-mot-passe---------------#
    
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def changePassMot(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe est bien modifier!')
            return redirect('profile')
        else:
            messages.error(request, 'SVP, il y a une erreur il faut le corriger.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


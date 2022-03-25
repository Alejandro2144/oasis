from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template.loader import get_template
from .forms import CustomUserCreationForm 

def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'home.html')

def tabla_historias(request):
    historias = HistoriaClinica.objects.all()
    return render(request, 'historias/tabla.html', {'historias': historias})

def historia(request, ID):
    historia = get_object_or_404(HistoriaClinica, pk=ID)
    return render(request, 'historias/historia.html', {'historia': historia})

def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username = formulario.cleaned_data['username'], password = formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request,"Se ha registrado correctamente")
            return redirect ('/home')
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)


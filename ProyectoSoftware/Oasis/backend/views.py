from django.shortcuts import render
from django.http import HttpResponse
from backend.models import HistoriaClinica

def home(request):
    return render(request, 'home.html')

def tabla_historias(request):
    historias = HistoriaClinica.objects.all()
    return render(request, 'historias/tabla.html', {'historias': historias})


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from backend.models import HistoriaClinica

def home(request):
    return render(request, 'home.html')

def tabla_historias(request):
    historias = HistoriaClinica.objects.all()
    return render(request, 'historias/tabla.html', {'historias': historias})

def historia(request, ID):
    historia = get_object_or_404(HistoriaClinica, pk=ID)
    return render(request, 'historias/historia.html', {'historia': historia})


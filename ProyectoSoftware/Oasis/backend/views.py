from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template.loader import get_template
from .forms import CustomUserCreationForm 
from django.http import HttpResponse
from backend.models import HistoriaClinica, InformacionPaciente, Usuario
from datetime import date
import json

def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'home.html')

def tabla_historias(request):
    historias = HistoriaClinica.objects.all()
    return render(request, 'historias/tabla.html', {'historias': historias})

def historia(request, ID):
    if request.method == 'POST':
        try:
            post = request.POST
            paciente, created = InformacionPaciente.objects.get_or_create(no_afiliacion=post.get('no_afiliacion',0))
            paciente.nombre=post.get('nombre', 0)
            paciente.tipo_afilliacion=post.get('tipo_afilliacion', 0)
            paciente.aseguradora=post.get('aseguradora', 0)
            paciente.edad=post.get('edad', 0)
            paciente.raza=post.get('raza', 0)
            paciente.etnicidad=post.get('etnicidad', 0)
            paciente.telefono=post.get('telefono', 0)
            paciente.save()
            historia = HistoriaClinica.objects.get(pk=ID)
            historia.paciente = paciente
            historia.motivo_de_consulta = post.get('motivo_de_consulta', 0)
            historia.enfermedad_actual = post.get('enfermedad_actual', 0)
            historia.antecedentes_morbidos = post.get('antecedentes_morbidos', 0)
            historia.antecedentes_ginecoobstétricos = post.get('antecedentes_ginecoobstétricos', 0)
            historia.medicamentos = post.get('medicamentos', 0)
            historia.alergias = post.get('alergias', 0)
            historia.antecedentes_sociales_personales = post.get('antecedentes_sociales_personales', 0)
            historia.antecedentes_familiares = post.get('antecedentes_familiares', 0)
            historia.inmunizaciones = post.get('inmunizaciones', 0)
            historia.revision_por_sistemas = post.get('revision_por_sistemas', 0)
            historia.epicrisis = post.get('epicrisis', 0)
            historia.dia_modificado = date.today()
            usuario = Usuario.objects.get(pk=request.user.id)
            historia.medico_encargado = usuario
            historia.motivo_actualizacion = post.get('motivo_actualizacion', 0)
            historia.firma = post.get('firma', 0)
            historia.save()
            messages.success(request, ('Your movie was successfully added!'))
        except:
            messages.error(request, 'Error saving form')
        return redirect("/historias")
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

def crear_historia(request):
    if request.method == 'POST':
        print(request.POST, flush=True)
        post = request.POST
        paciente, created = InformacionPaciente.objects.get_or_create(
            nombre=post.get('nombre', 0),
            tipo_afilliacion=post.get('tipo_afilliacion', 0),
            no_afiliacion=post.get('no_afiliacion',0),
            aseguradora=post.get('aseguradora', 0),
            edad=post.get('edad', 0),
            raza=post.get('raza', 0),
            etnicidad=post.get('etnicidad', 0),
            telefono=post.get('telefono', 0)
        )
        usuario = Usuario.objects.get(pk=request.user.id)
        HistoriaClinica.objects.create(
            paciente = paciente,
            motivo_de_consulta = post.get('motivo_de_consulta', 0),
            enfermedad_actual = post.get('enfermedad_actual', 0),
            antecedentes_morbidos = post.get('antecedentes_morbidos', 0),
            antecedentes_ginecoobstétricos = post.get('antecedentes_ginecoobstétricos', 0),
            medicamentos = post.get('medicamentos', 0),
            alergias = post.get('alergias', 0),
            antecedentes_sociales_personales = post.get('antecedentes_sociales_personales', 0),
            antecedentes_familiares = post.get('antecedentes_familiares', 0),
            inmunizaciones = post.get('inmunizaciones', 0),
            revision_por_sistemas = post.get('revision_por_sistemas', 0),
            epicrisis = post.get('epicrisis', 0),
            dia_creado = date.today(),
            dia_modificado = date.today(),
            medico_encargado = usuario,
            motivo_actualizacion = post.get('motivo_actualizacion', 0),
            firma = post.get('firma', 0)
        )
        messages.success(request, ('Se creó tu historia'))
        # except:
        #     messages.error(request, 'Error creando historia de usuario')
        return redirect("/historias")
    historia = {'pk': 'crear'}
    return render(request, 'historias/historia.html', {'historia': historia})

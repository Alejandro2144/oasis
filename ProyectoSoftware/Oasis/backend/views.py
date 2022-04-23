import email
from django.db.models import Q
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

def permisos(user_id,cargos):
    usuario = Usuario.objects.get(pk=user_id)
    passCheck = False
    for cargo in cargos:
        passCheck = passCheck or cargo == usuario.cargo
    return passCheck

def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'home.html')

def tabla_historias(request):
    if permisos(request.user.id,[Usuario.Cargos.Paciente, Usuario.Cargos.Investigador]):
        messages.error(request, "No tienes acceso a esta función")
        return redirect('/')
    buscar = request.GET
    if len(buscar) > 0:
        kwargs = {}
        if buscar.get('pk', 0) != "":
            kwargs['pk'] = int(buscar.get('pk', 0))
        if buscar.get('nombre', 0) != "":
            kwargs['paciente__nombre__contains'] = buscar.get('nombre', 0)
        if buscar.get('tipo_afiliacion', 0) != "":
            kwargs['paciente__tipo_afiliacion'] = buscar.get('tipo_afiliacion', 0)
        if buscar.get('no_afiliacion', 0) != "":
            kwargs['paciente__no_afiliacion'] = int(buscar.get('no_afiliacion', 0))
        if buscar.get('aseguradora', 0) != "":
            kwargs['paciente__aseguradora__contains'] = buscar.get('aseguradora', 0)
        if buscar.get('historia_clinica', 0) != "":
            historias = HistoriaClinica.objects.filter(Q(motivo_de_consulta__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(enfermedad_actual__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(antecedentes_morbidos__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(antecedentes_ginecoobstétricos__contains=buscar.get('historia_clinica', 0)) | 
                                                        Q(medicamentos__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(alergias__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(antecedentes_sociales_personales__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(inmunizaciones__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(revision_por_sistemas__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(epicrisis__contains=buscar.get('historia_clinica', 0)),**kwargs)
        else:
            historias = HistoriaClinica.objects.filter(**kwargs)
    else:
        historias = HistoriaClinica.objects.all()
    return render(request, 'historias/tabla.html', {'historias': historias})

def actualizar_o_crear_paciente(post, crear):
    paciente =  InformacionPaciente(no_afiliacion=post.get('no_afiliacion',0)) if crear else InformacionPaciente.objects.get(no_afiliacion=post.get('no_afiliacion',0))
    paciente.nombre=post.get('nombre', 0)
    paciente.tipo_afiliacion=post.get('tipo_afiliacion', 0)
    paciente.aseguradora=post.get('aseguradora', 0)
    paciente.edad=post.get('edad', 0)
    paciente.raza=post.get('raza', 0)
    paciente.etnicidad=post.get('etnicidad', 0)
    paciente.email=post.get('email', 0)
    paciente.telefono=post.get('telefono', 0)
    return paciente

def actualizar_o_crear_historia_clinica(post, ID , paciente, user_id):
    historia = HistoriaClinica.objects.get(pk=ID) if ID != None else HistoriaClinica()
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
    usuario = Usuario.objects.get(pk=user_id)
    historia.medico_encargado = usuario
    historia.firma = post.get('firma', 0)
    return historia

def ver_historia(request, ID):
    if request.method == 'POST':
        if not permisos(request.user.id,[Usuario.Cargos.Administrador, Usuario.Cargos.Medico, Usuario.Cargos.Secretaria]):
            messages.error(request, "No tienes acceso a esta función")
            return redirect('/')
        post = request.POST
        try:
            paciente = actualizar_o_crear_paciente(post, False)
            paciente.save()

            if permisos(request.user.id, [Usuario.Cargos.Secretaria]):
                messages.success(request, "Información actualizada")
                return redirect('/historias')

            historia = actualizar_o_crear_historia_clinica(post, ID, paciente, request.user.id)
            historia.motivo_actualizacion = post.get('motivo_actualizacion', 0)
            historia.save()
            messages.success(request, "Historia actualizada")
        except:
            messages.error(request, "Error actualizando historia")
        return redirect("/historias")

    if permisos(request.user.id,[Usuario.Cargos.Investigador]):
        messages.error(request, "No tienes acceso a esta función")
        return redirect('/')
    
    cargo = 0
    if permisos(request.user.id,[Usuario.Cargos.Secretaria]):
        cargo = 1
    if permisos(request.user.id,[Usuario.Cargos.Paciente]):
        cargo = 2

    # if permisos(request.user.id,[Usuario.Cargos.Paciente]):
    #     usuario = Usuario.objects.get(pk=request.user.id)
    #     if usuario.historia == ID:
    #         historia = get_object_or_404(HistoriaClinica, pk=ID)
    #         return render(request, 'historias/historia.html', {'historia': historia, 'tipos' : InformacionPaciente.TipoAfilliacion,'razas' : InformacionPaciente.Raza, 'cargo': cargo})
    #     else:
    #         messages.error(request, "No tienes acceso a esta función")
    #         return redirect('/')
    historia = get_object_or_404(HistoriaClinica, pk=ID)
    return render(request, 'historias/historia.html', {'historia': historia, 'tipos' : InformacionPaciente.TipoAfilliacion,'razas' : InformacionPaciente.Raza, 'cargo': cargo})

def registrar(request):
    if not permisos(request.user.id,[Usuario.Cargos.Administrador]):
        messages.error(request, "No tienes acceso a esta función")
        return redirect('/')
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
    if not permisos(request.user.id,[Usuario.Cargos.Administrador, Usuario.Cargos.Medico, Usuario.Cargos.Secretaria]):
        messages.error(request, "No tienes acceso a esta función")
        return redirect('/')

    if request.method == 'POST': 
        post = request.POST
        try:
            paciente = actualizar_o_crear_paciente(post, True)
            paciente.save()

            if permisos(request.user.id, [Usuario.Cargos.Secretaria]):
                messages.success(request, "Información actualizada")
                return redirect('/historias')
                
            historia = actualizar_o_crear_historia_clinica(post, None, paciente, request.user.id)
            historia.dia_creado = date.today()
            historia.save()
            messages.success(request, "Historia creada")
        except:
            messages.error(request, "Error creando historia")
        return redirect("/historias")
    historia = {'pk': 'crear'}
    return render(request, 'historias/historia.html', {'historia': historia, 'tipos' : InformacionPaciente.TipoAfilliacion,'razas' : InformacionPaciente.Raza})

def buscar_historia(request):
    if permisos(request.user.id,[Usuario.Cargos.Paciente]):
        messages.error(request, "No tienes acceso a esta función")
        return redirect('/')
    return render(request, "historias/buscar.html", {'tipos' : InformacionPaciente.TipoAfilliacion})

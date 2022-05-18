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
import csv
import datetime

def permisos(user_id,cargos):
    try:
        usuario = Usuario.objects.get(pk=user_id)
        passCheck = False
        for cargo in cargos:
            passCheck = passCheck or cargo == usuario.cargo
        return passCheck
    except:
        return False

def conseguir_barra_de_navegacion(user_id):
    try:
        usuario = Usuario.objects.get(pk=user_id)
        barra_navegacion = 0
        if permisos(user_id,[Usuario.Cargos.Medico, Usuario.Cargos.Secretaria]):
            barra_navegacion = 1
        if permisos(user_id,[Usuario.Cargos.Investigador]):
            barra_navegacion = 2
        if permisos(user_id,[Usuario.Cargos.Paciente]):
            barra_navegacion = 3
        return barra_navegacion
    except:
        return 4

def home(request):
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    print(barra_navegacion, flush=True)
    return render(request, 'home.html', {'barra_navegacion': barra_navegacion})

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
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    return render(request, 'historias/tabla.html', {'historias': historias, 'barra_navegacion': barra_navegacion})

def ver_informacion_investigador(request):
    buscar = request.GET
    if len(buscar) > 0:
        kwargs = {}
        if buscar.get('edad', 0) != "":
            kwargs['paciente__edad'] = int(buscar.get('edad', 0))
        if buscar.get('raza', 0) != "":
            kwargs['paciente__raza'] = buscar.get('raza', 0)
        if buscar.get('etnicidad', 0) != "":
            kwargs['paciente__etnicidad__contains'] = buscar.get('etnicidad', 0)
        if buscar.get('historia_clinica', 0) != "":
            numero_historias = len(HistoriaClinica.objects.filter(Q(motivo_de_consulta__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(enfermedad_actual__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(antecedentes_morbidos__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(antecedentes_ginecoobstétricos__contains=buscar.get('historia_clinica', 0)) | 
                                                        Q(medicamentos__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(alergias__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(antecedentes_sociales_personales__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(inmunizaciones__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(revision_por_sistemas__contains=buscar.get('historia_clinica', 0)) |
                                                        Q(epicrisis__contains=buscar.get('historia_clinica', 0)),**kwargs))
        else:
            numero_historias = len(HistoriaClinica.objects.filter(**kwargs))
    else:
        numero_historias = len(HistoriaClinica.objects.all())
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    return render(request, 'historias/busqueda_investigador.html', {'numero_historias': numero_historias, 'barra_navegacion': barra_navegacion})


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
        if permisos(request.user.id,[Usuario.Cargos.Investigador, Usuario.Cargos.Paciente]):
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
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    if permisos(request.user.id,[Usuario.Cargos.Paciente]):
        usuario = Usuario.objects.get(pk=request.user.id)
        historia = get_object_or_404(HistoriaClinica, pk=usuario.historia_id.pk)
        return render(request, 'historias/historia.html', {'historia': historia, 'tipos' : InformacionPaciente.TipoAfilliacion,'razas' : InformacionPaciente.Raza, 'cargo': cargo, 'barra_navegacion': barra_navegacion})
    historia = get_object_or_404(HistoriaClinica, pk=ID)
    return render(request, 'historias/historia.html', {'historia': historia, 'tipos' : InformacionPaciente.TipoAfilliacion,'razas' : InformacionPaciente.Raza, 'cargo': cargo, 'barra_navegacion': barra_navegacion})

def registrar(request):
    if permisos(request.user.id,[Usuario.Cargos.Medico, Usuario.Cargos.Secretaria, Usuario.Cargos.Investigador, Usuario.Cargos.Paciente]):
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
            usuario = Usuario.objects.get(pk=request.user.id)
            print("HIIIII",usuario.cargo, flush=True)
            if usuario.cargo == Usuario.Cargos.Paciente:
                return redirect('/historias/' + usuario.historia_id)
            messages.success(request,"Se ha registrado correctamente")
            return redirect ('/home')
        data["form"] = formulario
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    return render(request, 'registration/registro.html', data, {'barra_navegacion': barra_navegacion})

def crear_historia(request):
    if permisos(request.user.id,[Usuario.Cargos.Investigador, Usuario.Cargos.Paciente]):
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
            usuario = Usuario.objects.create(
                username=paciente.no_afiliacion,
                email=paciente.email,
                cargo=Usuario.Cargos.Paciente,
                first_name=paciente.nombre,
                historia_id=historia
            )
            usuario.set_password(paciente.no_afiliacion)
            usuario.save()
            messages.success(request, "Historia creada")
        except:
            messages.error(request, "Error creando historia")
        return redirect("/historias")
    cargo = 0
    if permisos(request.user.id,[Usuario.Cargos.Secretaria]):
        cargo = 1
    if permisos(request.user.id,[Usuario.Cargos.Paciente]):
        cargo = 2
    historia = {'pk': 'crear'}
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    return render(request, 'historias/historia.html', {'historia': historia, 'tipos' : InformacionPaciente.TipoAfilliacion,'razas' : InformacionPaciente.Raza, 'cargo': cargo,'barra_navegacion': barra_navegacion})

def buscar_historia(request):
    if permisos(request.user.id,[Usuario.Cargos.Paciente]):
        messages.error(request, "No tienes acceso a esta función")
        return redirect('/')
    cargo = 0
    if permisos(request.user.id,[Usuario.Cargos.Investigador]):
        cargo = 1
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    return render(request, "historias/buscar.html", {'tipos' : InformacionPaciente.TipoAfilliacion, 'razas' : InformacionPaciente.Raza, 'barra_navegacion': barra_navegacion, 'cargo': cargo})

def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = HistoriaClinica'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    keys = ["no_afiliacion","nombre","tipo_afiliacion","aseguradora","edad","raza","etnicidad","email","telefono",
    "motivo_de_consulta","enfermedad_actual","antecedentes_morbidos","antecedentes_ginecoobstétricos","medicamentos",
    "alergias","antecedentes_sociales_personales","antecedentes_familiares","inmunizaciones","revision_por_sistemas","epicrisis"]
    writer.writerow(keys)
    historias = HistoriaClinica.objects.all()

    for historia in historias:
        paciente = historia.paciente
        writer.writerow([paciente.no_afiliacion, paciente.nombre, paciente.tipo_afiliacion, paciente.aseguradora , paciente.edad, paciente.raza, 
        paciente.etnicidad, paciente.email, paciente.telefono, historia.motivo_de_consulta, historia.enfermedad_actual, historia.antecedentes_morbidos,
        historia.antecedentes_ginecoobstétricos, historia.medicamentos, historia.alergias, historia.antecedentes_sociales_personales, historia.antecedentes_familiares,
        historia.inmunizaciones, historia.revision_por_sistemas, historia.epicrisis])

    return response
def migrar_informacion(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('archivo').read().decode()
            lines = file.split("\n")
            first_line = True
            keys = ["no_afiliacion","nombre","tipo_afiliacion","aseguradora","edad","raza","etnicidad","email","telefono","motivo_de_consulta","enfermedad_actual","antecedentes_morbidos","antecedentes_ginecoobstétricos","medicamentos","alergias","antecedentes_sociales_personales","antecedentes_familiares","inmunizaciones","revision_por_sistemas","epicrisis"]
            csvFile = []
            for line in lines:
                if first_line:
                    pass
                dic = {}
                values = line.split(",")
                for i in range(len(keys)):
                    dic[keys[i]] = values[i]
                csvFile.append(dic.copy())
            first_line = True
            for rows in csvFile:
                if first_line:
                    first_line = False
                    continue
                paciente = actualizar_o_crear_paciente(rows, True)
                paciente.save()
                historia = actualizar_o_crear_historia_clinica(rows, None, paciente, request.user.id)
                historia.dia_creado = date.today()
                historia.save()
                usuario = Usuario.objects.create(
                    username=paciente.no_afiliacion,
                    email=paciente.email,
                    cargo=Usuario.Cargos.Paciente,
                    first_name=paciente.nombre,
                    historia_id=historia
                )
                usuario.set_password(paciente.no_afiliacion)
                usuario.save()
            messages.success(request, "Migración exitosa")
            return redirect('/')
        except:
            messages.error(request, "Migración fallida")
            return redirect('/')
    barra_navegacion = conseguir_barra_de_navegacion(request.user.id)
    return render(request, "migracion.html", {'barra_navegacion': barra_navegacion})

from django.contrib.auth.models import AbstractUser
from django.db import models
from sklearn.preprocessing import maxabs_scale

# Create your models here.

class Usuario(AbstractUser):
    class Cargos(models.TextChoices):
        Medico = "Medico"
        Investigador = "Investigador"
        Administrador = "Administrador"
        Paciente = "Paciente"
        Secretaria = "Secretaria"
    cargo = models.CharField(max_length=20, choices=Cargos.choices, default = Cargos.Paciente)


class InformacionPaciente(models.Model):
    class TipoAfilliacion(models.TextChoices):
        Cedula = "CC"
        TarjetaIdentidad = "TI"
        Pasaporte = "PA"
    class Raza(models.TextChoices):
        Blanco = "Blanco"
        Negro = "Negro"
        Mestizo = "Mestizo"
    nombre = models.CharField(max_length=255)
    tipoAfilliacion = models.CharField(max_length=2, choices=TipoAfilliacion.choices, default=TipoAfilliacion.Cedula)
    noAfiliacion = models.BigIntegerField()
    aseguradora = models.CharField(max_length=255)
    edad = models.IntegerField()
    raza = models.CharField(max_length=20, choices=Raza.choices, default=Raza.Blanco)
    etnicidad = models.EmailField()
    telefono = models.BigIntegerField()


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(InformacionPaciente, on_delete=models.CASCADE)
    motivo_de_consulta = models.TextField(null = False, blank = False)
    enfermedad_actual = models.TextField(null = False, blank=False)
    antecedentes_morbidos = models.TextField(null = False, blank = False)
    antecedentes_ginecoobstétricos = models.TextField(null = False, blank = False)
    medicamentos = models.TextField(null = False, blank = False)
    alergias = models.TextField(null = False, blank = False)
    antecedentes_sociales_personales = models.TextField(null = True, blank = True)
    antecedentes_familiares = models.TextField(null = True, blank = True)
    inmunizaciones = models.TextField(null = True, blank = True)
    Revision_por_sistemas = models.TextField(null = False, blank = False)
    Epicrisis = models.TextField(null = False, blank = False)
    dia_creado = models.DateField(null = False, blank = False)
    dia_modificado = models.DateField(null = False, blank = False)
    medico_encargado = models.DateField(null = False, blank = False)
    motivo_actualizacion = models.TextField(null = False, blank =False)
    firma = models.ImageField(upload_to = "firmas")
    
    
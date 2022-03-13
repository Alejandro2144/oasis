from django.contrib import admin
from .models import Usuario, HistoriaClinica, InformacionPaciente

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(InformacionPaciente)
class InformacionPacienteAdmin(admin.ModelAdmin):
    pass

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    pass
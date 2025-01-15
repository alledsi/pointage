from django.contrib import admin
from .models import pointage

# Register your models here.
@admin.register(pointage)
class pointAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'matricule', 'agent', 'arrivee', 'locarrivee', 'debutpause', 'locdebutpause', 'finpause', 'locfinpause', 'depart', 'locdepart')
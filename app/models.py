from django.db import models

# Create your models here.

class pointage(models.Model):
    date = models.CharField(max_length=100)
    matricule = models.CharField(max_length=100)
    agent = models.CharField(max_length=100)
    arrivee = models.CharField(max_length=100)
    locarrivee = models.CharField(max_length=100, null=True)
    depart = models.CharField(max_length=100, null=True)
    locdepart = models.CharField(max_length=100, null=True)

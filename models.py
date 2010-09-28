# -*- coding: utf-8 -*-
from django.db import models
from gestib.models import *


class Assignatura(models.Model):
	grup = models.ManyToManyField(Grup)
	nom = nom = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nom





class GrupNota(models.Model):
	nom = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nom



class TipNota(models.Model):
	nom = models.CharField(max_length=100)
	ordre = models.IntegerField()
	grupNota = models.ForeignKey(GrupNota)
	
	class Meta:
		ordering = ('-nom',)
	
	def __unicode__(self):
		return self.nom



class ItemNota(models.Model):
	it = models.CharField(max_length=100)
	grupNota = models.ForeignKey(GrupNota)
	
	class Meta:
		ordering = ('-it',)
	
	def __unicode__(self):
		return self.it + "|" + self.grupNota.nom







class Nota(models.Model):
	nota = models.ForeignKey(ItemNota)
	tipnota = models.ForeignKey(TipNota)
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Assignatura)


	def __unicode__(self):
		return self.nota.it + " | " + self.tipnota.nom + " | " + self.alumne.nom + " | " + self.assignatura.nom


class Comentari(models.Model):
	text = models.TextField()
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Assignatura)
	
	class Meta:
		ordering = ('-text',)
	
	def __unicode__(self):
		return self.text




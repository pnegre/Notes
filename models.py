# -*- coding: utf-8 -*-
from django.db import models
from gestib.models import *



class TipNota(models.Model):
	nom = models.CharField(max_length=100)
	ordre = models.IntegerField()
	
	class Meta:
		ordering = ('-nom',)
	
	def __unicode__(self):
		return self.nom


class ItemNota(models.Model):
	it = models.CharField(max_length=100)
	tipnota = models.ForeignKey(TipNota)
	
	class Meta:
		ordering = ('-it',)
	
	def __unicode__(self):
		return self.it + "|" + self.tipnota.nom
	


class Nota(models.Model):
	nota = models.ForeignKey(ItemNota)
	tipnota = models.ForeignKey(TipNota)
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Submateria)


	def __unicode__(self):
		return self.nota.it + " | " + self.tipnota.nom + " | " + self.alumne.nom + " | " + self.assignatura.nom


class Comentari(models.Model):
	text = models.TextField()
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Submateria)
	
	class Meta:
		ordering = ('-text',)
	
	def __unicode__(self):
		return self.text




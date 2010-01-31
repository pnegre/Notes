# -*- coding: utf-8 -*-
from django.db import models


class Curs(models.Model):
	nom = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.nom

class Assignatura(models.Model):
	nom = models.CharField(max_length=200)
	curs = models.ForeignKey(Curs)

	def __unicode__(self):
		return self.nom


class Alumne(models.Model):
	nom = models.CharField(max_length=200)
	curs = models.ForeignKey(Curs)
	
	def __unicode__(self):
		return self.nom


class TipNota(models.Model):
	nom = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nom

class ItemNota(models.Model):
	it = models.CharField(max_length=100)
	tipnota = models.ForeignKey(TipNota)
	
	def __unicode__(self):
		return self.it + "|" + self.tipnota.nom
	


class Nota(models.Model):
	nota = models.ForeignKey(ItemNota)
	tipnota = models.ForeignKey(TipNota)
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Assignatura)


	#def __unicode__(self):
		#return self.nota


class Comentari(models.Model):
	text = models.TextField()
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Assignatura)
	
	def __unicode__(self):
		return self.text




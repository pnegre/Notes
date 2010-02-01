# -*- coding: utf-8 -*-
from django.db import models


class Curs(models.Model):
	nom = models.CharField(max_length=200)
	tutor = models.CharField(max_length=300)
	
	class Meta:
		ordering = ('-nom',)
	
	def __unicode__(self):
		return self.nom

class Assignatura(models.Model):
	nom = models.CharField(max_length=200)
	curs = models.ForeignKey(Curs)
	
	class Meta:
		ordering = ('-nom',)

	def __unicode__(self):
		return self.nom + " | " + self.curs.nom


class Alumne(models.Model):
	nom = models.CharField(max_length=200)
	l1 = models.CharField(max_length=200)
	l2 = models.CharField(max_length=200)
	curs = models.ForeignKey(Curs)
	
	class Meta:
		ordering = ('-l1','l2')
	
	def __unicode__(self):
		return self.l1 + " " + self.l2 + ", "+ self.nom


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




# -*- coding: utf-8 -*-
from django.db import models
from gestib.models import *



class Periode(models.Model):
	nom = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nom



class PeriodeActiu(models.Model):
	periode = models.ForeignKey(Periode)



class GrupsPermesos(models.Model):
	SHOW_CHOICES = (
		(u'S', u'Si'),
		(u'N', u'No'),
	)
	grup = models.ForeignKey(Grup)
	mostrar = models.CharField(max_length=1, choices=SHOW_CHOICES)
	
	def __unicode__(self):
		return self.grup.curs.nom + self.grup.nom + " " + self.mostrar
	
	class Meta:
		ordering = ('grup',)



class Assignatura(models.Model):
	grup = models.ManyToManyField(Grup)
	nom = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.nom
	
	class Meta:
		ordering = ('nom',)



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
		return self.it + " | " + self.grupNota.nom



class Nota(models.Model):
	nota = models.ForeignKey(ItemNota)
	tipnota = models.ForeignKey(TipNota)
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Assignatura)
	periode = models.ForeignKey(Periode)

	def __unicode__(self):
		return self.nota.it + " | " + self.tipnota.nom + " | " + self.alumne.nom + " | " + self.assignatura.nom + " | " + self.periode.nom
	
	class Meta:
		permissions = (
			("posar_notes","Pot posar notes"),
			("impr_butlletins","Pot imprimir butlletins"),
		)



class Comentari(models.Model):
	text = models.TextField()
	alumne = models.ForeignKey(Alumne)
	assignatura = models.ForeignKey(Assignatura)
	periode = models.ForeignKey(Periode)
	
	class Meta:
		ordering = ('-text',)
	
	def __unicode__(self):
		return self.text




# -*- coding: utf-8 -*-
from django.db import models
from gestib.models import *


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


class InterAvaluacio(models.Model):
	nom = models.CharField(max_length=100)
	nomButlleti = models.CharField(max_length=100, blank=True, null=True)
	anny = models.ForeignKey(Any)
	data1 = models.DateField()
	data2 = models.DateField()

	grups = models.ManyToManyField(Grup, blank=True, null=True)
	tipnotes = models.ManyToManyField(TipNota, blank=True, null=True)

	def __unicode__(self):
		return str(self.anny) + ' ' + self.nom


class Config(models.Model):
	interactiva = models.ForeignKey(InterAvaluacio)






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
	# assignatura = models.ForeignKey(Assignatura)
	submateria = models.ForeignKey(Submateria)
	interavaluacio = models.ForeignKey(InterAvaluacio)

	def __unicode__(self):
		return self.nota.it + " | " + self.tipnota.nom + " | " + self.alumne.nom + " | " + self.submateria.nom + " | " + str(self.interavaluacio)

	class Meta:
		permissions = (
			("posar_notes","Pot posar notes"),
			("impr_butlletins","Pot imprimir butlletins"),
		)


class Comentari(models.Model):
	text = models.TextField()
	alumne = models.ForeignKey(Alumne)
	submateria = models.ForeignKey(Submateria)
	interavaluacio = models.ForeignKey(InterAvaluacio)

	class Meta:
		ordering = ('-text',)

	def __unicode__(self):
		return self.text

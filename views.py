# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

#import datetime
#import re

from notes.models import *
from gestib.models import *

from notes.aux import butlletins_per_grup_i_alumne


def curs(request,curs_id):
	pass
	#curs = Curs.objects.filter(id=curs_id)[0]
	
	#if request.method == "POST":
		#fields = request.POST
		#if 'newal' in fields.keys():
			#al = Alumne(nom=fields['al'], l1=fields['l1'], l2=fields['l2'], curs=curs)
			#al.save()
		#elif 'newass' in fields.keys():
			#ass = Assignatura(nom=fields['ass'], curs=curs)
			#ass.save()
	
	#asgs = Assignatura.objects.filter(curs=curs)
	#als = Alumne.objects.filter(curs=curs).order_by('l1')
	#tipnotes = TipNota.objects.all().order_by('ordre')
	#items = ItemNota.objects
	#notes = Nota.objects
	
	#ntip=0
	#for i in tipnotes:
		#ntip += 1
					
	#return render_to_response(
			#'notes/curs.html', { 
				#'curs': curs,
				#'asgs': asgs,
				#'alumnes': als,
				#'tipnotes': tipnotes,
				#'items': items,
				#'ntip': ntip,
	#} )



def assig(request,as_id,gr_id):
	assignatura = Assignatura.objects.filter(id=as_id)[0]
	grup = Grup.objects.filter(id=gr_id)[0]
	tipnotes = TipNota.objects.all().order_by('ordre')
	als = Alumne.objects.filter(grup=grup)
	periode = PeriodeActiu.objects.all()[0].periode
	
	for a in als:
		c = Comentari.objects.filter(alumne=a,assignatura=assignatura,periode=periode)
		if (c):
			a.comm = c[0].text
		else:
			a.comm = ''
	
	return render_to_response(
			'notes/assignatura.html', { 
				'grup': grup,
				'assignatura': assignatura,
				'alumnes': als,
				'tipnotes': tipnotes,
	} )



def llistat_cursos(request):
	grups = []
	permesos = GrupsPermesos.objects.all()
	if permesos:
		for p in permesos:
			if p.mostrar == 'S':
				grups.append(p.grup)
			
	#grups = Grup.objects.all()
	return render_to_response(
			'notes/index.html', { 
				'grups': grups,
	} )	






def butlleti(request,grup_id):
	grup = Grup.objects.filter(id=grup_id)[0]
	alumnes = Alumne.objects.filter(grup=grup).order_by('llinatge1')
	
	return butlletins_per_grup_i_alumne(grup,alumnes)



def butlletins2(request):
	grups = []
	permesos = GrupsPermesos.objects.all()
	if permesos:
		for p in permesos:
			if p.mostrar == 'S':
				grups.append(p.grup)
				
	return render_to_response(
			'notes/butlletins.html', {
				'grups': grups,
	} )



def butlletins_individuals(request):
	pass
	#if request.POST:
		#als = []
		#fields = request.POST
		#curs = Curs.objects.filter(id=fields['curs'])[0]
		#bb = fields['1']
		#for f in fields:
			#if re.match(f,'^\d+$'): 
				#als.append(Alumne.objects.filter(id=int(f)))
		
		#return butlletins_per_curs_i_alumne(curs,als)
	
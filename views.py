# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

#import datetime
#import re

from notes.models import *
from gestib.models import *

from notes.aux import butlletins_per_curs_i_alumne


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
	
	#for a in als:
		#c = Comentari.objects.filter(alumne=a,assignatura=assignatura)
		#if (c):
			#a.comm = c[0].text
		#else:
			#a.comm = ''
	
	return render_to_response(
			'notes/assignatura.html', { 
				'grup': grup,
				'assignatura': assignatura,
				'alumnes': als,
				'tipnotes': tipnotes,
	} )



def llistat_cursos(request):
	grups = Grup.objects.all()
	return render_to_response(
			'notes/index.html', { 
				'grups': grups,
	} )	




def upload(request):
	pass
	#cursos = Curs.objects.all()
	#r = ""
	#if request.method == 'POST':
		#curs = Curs.objects.filter(id=request.POST['curs'])[0]
		#f = request.FILES['file']
		#ct = ""
		#for chunk in f.chunks():
			#ct += chunk
		#lines = ct.split("\n")
		#for l in lines:
			#s = l.split(",")
			#if len(s) < 4: continue
			#l1 = re.sub('"','',s[0])
			#l2 = re.sub('"','',s[1])
			#nom = re.sub('"','',s[2])
			#r += l1 + " " + l2 + " " + nom + " ||| "
			#alumne = Alumne(
				#l1 = l1,
				#l2 = l2,
				#nom = nom,
				#curs = curs
			#)
			#alumne.save()
			
	#return render_to_response(
			#'notes/upload.html', {
				#'content': r,
				#'cursos': cursos, 
	#} )



def butlleti(request,curs_id):
	pass
	#curs = Curs.objects.filter(id=curs_id)[0]
	#alumnes = Alumne.objects.filter(curs=curs).order_by('l1')
	
	#return butlletins_per_curs_i_alumne(curs,alumnes)



def butlletins2(request):
	pass
	#cursos = Curs.objects.all()
	#return render_to_response(
			#'notes/butlleti.html', {
				#'cursos': cursos, 
	#} )



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
	
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from notes.models import *

def curs(request,curs_id):
	curs = Curs.objects.filter(id=curs_id)[0]
	
	if request.method == "POST":
		fields = request.POST
		if 'newal' in fields.keys():
			al = Alumne(nom=fields['al'], curs=curs)
			al.save()
		elif 'newass' in fields.keys():
			ass = Assignatura(nom=fields['ass'], curs=curs)
			ass.save()
	
	asgs = Assignatura.objects.filter(curs=curs)
	als = Alumne.objects.filter(curs=curs)
	tipnotes = TipNota.objects.all()
	items = ItemNota.objects
	notes = Nota.objects
					
	return render_to_response(
			'notes/curs.html', { 
				'curs': curs,
				'asgs': asgs,
				'alumnes': als,
				'tipnotes': tipnotes,
				'items': items,
				'notes': notes,
	} )


def nnota(request,al_id,as_id,it_id,tn_id):
	tipnota = TipNota.objects.filter(id=tn_id)[0]
	alumne = Alumne.objects.filter(id=al_id)[0]
	assignatura = Assignatura.objects.filter(id=as_id)[0]
	qualif = ItemNota.objects.filter(id=it_id)[0]
	try:
		nota = Nota.objects.filter(tipnota=tipnota,alumne=alumne,assignatura=assignatura)[0]
		nota.nota = qualif
		nota.save()
	except:
		nota = Nota(
			nota = qualif,
			tipnota = tipnota,
			alumne = alumne,
			assignatura = assignatura
		)
		nota.save()
		
	return HttpResponse()


#def getnota(request,al_id,as_id,tn_id):
	#tipnota = TipNota.objects.filter(id=tn_id)[0]
	#alumne = Alumne.objects.filter(id=al_id)[0]
	#assignatura = Assignatura.objects.filter(id=as_id)[0]
	
	#nota = Nota.objects.filter(tipnota=tipnota,alumne=alumne,assignatura=assignatura)[0]
	#return HttpResponse(simplejson.dumps( {'nota': nota.nota.id} ), mimetype='application/javascript')


def llistat_cursos(request):
	cursos = Curs.objects.all()
	return render_to_response(
			'notes/index.html', { 
				'cursos': cursos,
	} )
	


def getnotes(request,curs_id):
	notes = Nota.objects.filter(id=curs_id)
	curs = Curs.objects.filter(id=curs_id)
	r = {}
	als = Alumne.objects.filter(curs=curs)
	asgs = Assignatura.objects.filter(curs=curs)
	tipnotes = TipNota.objects.all()
	for a in als:
		r1 = {}
		for asg in asgs:
			r2 = {}
			for t in tipnotes:
				try:
					n = Nota.objects.filter(assignatura=asg,alumne=a,tipnota=t)[0]
					r2[t.id] = n.nota.id
				except:
					r2[t.id] = None
			r1[asg.id] = r2
		r[a.id] = r1
		
	return HttpResponse(simplejson.dumps( r ), mimetype='application/javascript')
	
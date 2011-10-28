# -*- coding: utf-8 -*-

from functools import wraps

from django.contrib.auth.decorators import login_required, permission_required

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.decorators import available_attrs

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from notes.models import *

import re



def permission_required_403(perm):
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if request.user.has_perm(perm):
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponseForbidden('forbidden');
				#resp = render_to_response('403.html', context_instance=RequestContext(request))
				#resp.status_code = 403
				#return resp
		
		return _wrapped_view
	return decorator








def getPeriode():
	return Config.objects.all()[0].periodeActiu

def esPodenPosarNotes():
	if Config.objects.all()[0].escriureNotes == 'S':
		return True
	else:
		return False


@permission_required('notes.posar_notes')
def comentari(request):
	if esPodenPosarNotes() == False: return HttpResponse()
	
	post = request.POST
	periode = getPeriode()
	text = post['comentari']
	alumne = Alumne.objects.filter(id=int(post['al']))[0]
	assignatura = Assignatura.objects.filter(id=int(post['as']))[0]
	
	if not re.match('^\s*$', text):
		try:
			com = Comentari.objects.filter(alumne=alumne, assignatura=assignatura,periode=periode)[0]
			com.text = text
			com.save()
		except:
			com = Comentari(
				text = text,
				alumne = alumne,
				assignatura = assignatura,
				periode=periode,
			)
			com.save()
	else:
		try:
			com = Comentari.objects.filter(alumne=alumne, assignatura=assignatura, periode=periode)[0]
			com.delete()
		except:
			pass
		
	return HttpResponse()



@permission_required_403('notes.posar_notes')
def nnota(request):
	if esPodenPosarNotes() == False: return HttpResponse()
	
	fields = request.POST
	periode = getPeriode()
	tipnota = TipNota.objects.filter(id=fields['tnota'])[0]
	alumne = Alumne.objects.filter(id=fields['alumne'])[0]
	assignatura = Assignatura.objects.filter(id=fields['assignatura'])[0]
	if fields['nota'] == "-1":
		nota = Nota.objects.filter(tipnota=tipnota,alumne=alumne,assignatura=assignatura,periode=periode)[0]
		nota.delete()
		return HttpResponse()
		
	qualif = ItemNota.objects.filter(id=fields['nota'])[0]
	
	try:
		nota = Nota.objects.filter(tipnota=tipnota,alumne=alumne,assignatura=assignatura,periode=periode)[0]
		nota.nota = qualif
		nota.save()
	except:
		nota = Nota(
			nota = qualif,
			tipnota = tipnota,
			alumne = alumne,
			assignatura = assignatura,
			periode=periode,
		)
		nota.save()
		
	return HttpResponse()



# Donat un curs i una assignatura, torna totes les notes d'aquella assignatura, en json
@permission_required('notes.posar_notes')
def getnotes(request,grup_id,as_id):
	periode = getPeriode()
	grup = Curs.objects.filter(id=grup_id)[0]
	r = {}
	als = Alumne.objects.filter(grup=grup)
	asg = Assignatura.objects.filter(id=as_id)[0]
	tipnotes = TipNota.objects.all()
	for a in als:
		r1 = {}
		for t in tipnotes:
			try:
				n = Nota.objects.filter(assignatura=asg,alumne=a,tipnota=t,periode=periode)[0]
				r1[t.id] = n.nota.id
			except:
				r1[t.id] = None
		
		r[a.id] = r1
		
	return HttpResponse(simplejson.dumps( r ), mimetype='application/javascript')



@permission_required('notes.posar_notes')
def llista_alumnes(request,curs_id):
	pass
	#curs = Curs.objects.filter(id=curs_id)[0]
	#alumnes = Alumne.objects.filter(curs=curs)
	#r = {}
	#for a in alumnes:
		#r[a.id] = str(a)
	
	#return HttpResponse(simplejson.dumps( r ), mimetype='application/javascript')

# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext

from django.contrib.auth.decorators import login_required, permission_required

from notes.models import *
from gestib.models import *

from notes.aux import butlletins_per_grup_i_alumne


@permission_required('notes.posar_notes')
def assig(request,as_id,gr_id):
	
	class NObj(object):
		pass
	
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
		
		notes = []
		for t in tipnotes:
			o = NObj()
			o.tipnota = t
			n = Nota.objects.filter(assignatura=assignatura,alumne=a,tipnota=t,periode=periode)
			if not n: 
				o.nota = None
			else:
				o.nota = n[0]
			notes.append(o)
		
		a.notes = notes
	
	return render_to_response(
			'notes/assignatura.html', { 
				'grup': grup,
				'assignatura': assignatura,
				'alumnes': als,
				'tipnotes': tipnotes,
			}, context_instance=RequestContext(request))



@permission_required('notes.posar_notes')
def llistat_cursos(request):
	grups = []
	permesos = GrupsPermesos.objects.all()
	if permesos:
		for p in permesos:
			if p.mostrar == 'S':
				grups.append(p.grup)
			
	return render_to_response(
			'notes/index.html', { 
				'grups': grups,
			}, context_instance=RequestContext(request) )



@permission_required('notes.impr_butlletins')
def butlleti(request,grup_id):
	grup = Grup.objects.filter(id=grup_id)[0]
	alumnes = Alumne.objects.filter(grup=grup).order_by('llinatge1')
	
	return butlletins_per_grup_i_alumne(grup,alumnes)



@permission_required('notes.impr_butlletins')
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
			}, context_instance=RequestContext(request) )



@permission_required('notes.impr_butlletins')
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
	
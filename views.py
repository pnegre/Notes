# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext

from django.contrib.auth.decorators import login_required, permission_required

from notes.models import *
from gestib.models import *

import datetime

import aux


def getActiveInter():
	# TODO: marcar interavaluació activa d'alguna manera...
	iact = Config.objects.all()[0]
	return iact.interactiva


def getAlumnes(grup, anny):
	als = []
	for m in Matricula.objects.filter(grup=grup,anny=anny):
		als.append(m.alumne)
	return sorted(als, key=lambda al: al.llinatge1)


def getAssignaturesGrup(grup, inter):
	assigs = []
	for a in Assignatura.objects.all():
		try:
			AssignaturaGrupInter.objects.get(assignatura=a, grup=grup, interavaluacio=inter)
			assigs.append(a)
		except AssignaturaGrupInter.DoesNotExist:
			pass
	return assigs


@permission_required('notes.posar_notes')
def llistat_cursos(request):
	inter = getActiveInter()
	grups = inter.grups.all()

	for g in grups:
		g.assignatures = getAssignaturesGrup(g, inter)

	return render_to_response(
			'notes/index.html', {
				'grups': grups,
				'inter': inter,
			}, context_instance=RequestContext(request) )

# Administrar assignatures dels cursos d'una interavaluació
@permission_required('is_superuser')
def admin(request):
	return render_to_response(
		'notes/admin1.html', { },
		context_instance=RequestContext(request)
	)

# Administrar cursos d'una interavaluació
@permission_required('is_superuser')
def admin2(request):
	return render_to_response(
		'notes/admin2.html', { },
		context_instance=RequestContext(request)
	)


@permission_required('notes.posar_notes')
def grupsAny(request, inter_id):
	interid = request.POST.get("inter")
	inter = InterAvaluacio.objects.get(id=inter_id)
	anny = inter.anny
	grups = Grup.objects.filter(curs__anny=anny)
	ginter = inter.grups
	for g in grups:
		try:
			ginter.get(id=g.id)
			g.checked = True
		except:
			pass

	return render_to_response(
		'notes/grupsinter.html', {
			'grups': grups,
			'inter': inter,
		}
	)



@permission_required('notes.posar_notes')
def assig(request,inter_id, as_id,gr_id):

	class NObj(object):
		pass

	assignatura = Assignatura.objects.get(id=as_id)
	grup = Grup.objects.get(id=gr_id)
	inter = InterAvaluacio.objects.get(id=inter_id)

	tipnotes = TipNota.objects.all().order_by('ordre')
	als = getAlumnes(grup, inter.anny)

	for a in als:
		c = Comentari.objects.filter(alumne=a,assignatura=assignatura,interavaluacio=inter)
		if (c):
			a.comm = c[0].text
		else:
			a.comm = ''

		notes = []
		for t in tipnotes:
			o = NObj()
			o.tipnota = t
			n = Nota.objects.filter(assignatura=assignatura,alumne=a,tipnota=t,interavaluacio=inter)
			if not n:
				o.nota = None
			else:
				o.nota = n[0]
			notes.append(o)

		a.notes = notes

	desactivat = False
	dt = datetime.datetime.now().date()
	if dt < inter.data1 or dt > inter.data2:
		desactivat = True

	print desactivat

	return render_to_response(
			'notes/assignatura.html', {
				'grup': grup,
				'assignatura': assignatura,
				'alumnes': als,
				'tipnotes': tipnotes,
				'inter': inter,
				'desactivat': desactivat,
			}, context_instance=RequestContext(request))




@permission_required('notes.impr_butlletins')
def butlleti(request, inter_id, grup_id):
	inter = InterAvaluacio.objects.get(id=inter_id)
	grup = Grup.objects.get(id=grup_id)
	alumnes = getAlumnes(grup, inter.anny)
	assignatures = getAssignaturesGrup(grup, inter)
	return aux.butlletins_per_grup_i_alumne(inter, assignatures, grup, alumnes)



@permission_required('notes.impr_butlletins')
def butlletins2(request):
	inter = getActiveInter()
	grups = inter.grups.all()

	return render_to_response(
			'notes/butlletins.html', {
				'grups': grups,
				'inter': inter,
			}, context_instance=RequestContext(request) )

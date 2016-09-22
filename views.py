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

#
# def getAssignaturesGrup(grup, inter):
# 	assigs = []
# 	for a in Assignatura.objects.all():
# 		try:
# 			AssignaturaGrupInter.objects.get(assignatura=a, grup=grup, interavaluacio=inter)
# 			assigs.append(a)
# 		except AssignaturaGrupInter.DoesNotExist:
# 			pass
# 	return assigs

#
# @permission_required('notes.posar_notes')
# def llistat_cursos(request):
# 	inter = getActiveInter()
# 	grups = inter.grups.all()
#
# 	for g in grups:
# 		g.assignatures = getAssignaturesGrup(g, inter)
#
# 	return render_to_response(
# 			'notes/index.html', {
# 				'grups': grups,
# 				'inter': inter,
# 			}, context_instance=RequestContext(request) )

@permission_required('notes.posar_notes')
def llistat_cursos(request):
	return render_to_response(
				'notes/index2.html', {
				}, context_instance=RequestContext(request) )

# Administrar assignatures dels cursos d'una interavaluació
@permission_required('is_superuser')
def admin(request):
	return render_to_response(
		'notes/admin1.html', { },
		context_instance=RequestContext(request)
	)

# # Administrar cursos d'una interavaluació
# @permission_required('is_superuser')
# def admin2(request):
# 	return render_to_response(
# 		'notes/admin2.html', { },
# 		context_instance=RequestContext(request)
# 	)

# Administrar cursos d'una interavaluació
@permission_required('is_superuser')
def adminInter(request):
	return render_to_response(
		'notes/adminInter.html', { },
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
def assig2(request,inter_id, as_id,gr_id):
	return render_to_response(
			'notes/assignatura2.html', {

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
	return render_to_response(
			'notes/nouButlletins.html', {
			}, context_instance=RequestContext(request) )

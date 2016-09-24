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


@permission_required('notes.posar_notes')
def llistat_cursos(request):
	return render_to_response(
				'notes/index2.html', {
				}, context_instance=RequestContext(request) )


# Administrar cursos d'una interavaluació
@permission_required('is_superuser')
def adminInter(request):
	return render_to_response(
		'notes/adminInter.html', { },
		context_instance=RequestContext(request)
	)


@permission_required('notes.impr_butlletins')
def butlletins2(request):
	return render_to_response(
			'notes/nouButlletins.html', {
			}, context_instance=RequestContext(request) )


@permission_required('notes.impr_butlletins')
def butlletiPDF(request, inter_id, grup_id):
	inter = InterAvaluacio.objects.get(id=inter_id)
	grup = Grup.objects.get(id=grup_id)
	submateries = grup.submateries.all()
	alumnes = []
	for m in Matricula.objects.filter(grup=grup,anny=inter.anny):
		alumnes.append(m.alumne)

	return aux.butlletins_per_grup_i_alumne(inter, submateries, grup, alumnes)


@permission_required('is_superuser')
def editSubsView(request):
	return render_to_response(
		'notes/editsubs.html', { },
		context_instance=RequestContext(request)
	)

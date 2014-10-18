# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext

from django.contrib.auth.decorators import login_required, permission_required

from notes.models import *
from gestib.models import *


def getActiveInter():
	# TODO: marcar interavaluació activa d'alguna manera...
	i = InterAvaluacio.objects.all()[0]
	return i

def getSubmateries(grup):
	result = []
	sgrup = SubmateriaGrup.objects.filter(grup=grup)
	for sg in sgrup:
		result.append(sg.submateria)

	return result


@permission_required('notes.posar_notes')
def llistat_cursos(request):
	inter = getActiveInter()
	grups = inter.grups.all()

	for g in grups:
		g.assignatures = getSubmateries(g)

	return render_to_response(
			'notes/index.html', {
				'grups': grups,
			}, context_instance=RequestContext(request) )

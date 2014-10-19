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


@permission_required('notes.posar_notes')
def llistat_cursos(request):
	inter = getActiveInter()
	grups = inter.grups.all()

	for g in grups:
		g.assignatures = []
		for a in Assignatura.objects.all():
			try:
				AssignaturaGrupInter.objects.get(assignatura=a, grup=g, interavaluacio=inter)
				g.assignatures.append(a)
			except AssignaturaGrupInter.DoesNotExist:
				pass

	return render_to_response(
			'notes/index.html', {
				'grups': grups,
				'inter': inter,
			}, context_instance=RequestContext(request) )

@permission_required('is_superuser')
def admin(request):
	return render_to_response(
		'notes/admin1.html', { },
		context_instance=RequestContext(request)
	)


#
#
# @permission_required('notes.posar_notes')
# def assig(request,as_id,gr_id):
#
# 	return render_to_response(
# 			'notes/assignatura.html', {
# 				'grup': grup,
# 				'assignatura': assignatura,
# 				'alumnes': als,
# 				'tipnotes': tipnotes,
# 				'activat': not esPodenPosarNotes(),
# 			}, context_instance=RequestContext(request))

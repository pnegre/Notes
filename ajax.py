# -*- coding: utf-8 -*-

from functools import wraps

from django.contrib.auth.decorators import login_required, permission_required

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.decorators import available_attrs

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from notes.models import *
from gestib.models import *

import re, datetime


# Mira si la data actual està dins el rang [ inter.data1, inter.data2 ]
def dateInter(inter):
	dt = datetime.datetime.now().date()
	if dt < inter.data1 or dt > inter.data2:
		return False
	return True


# Custom decorator.
# Envia un codi 403 (forbidden) enlloc de redirigir a login
# Això va molt bé per les cridades AJAX
def permission_required_403(perm):
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if request.user.has_perm(perm):
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponseForbidden('forbidden');

		return _wrapped_view
	return decorator


@permission_required_403('notes.posar_notes')
def anys(request):
	annys = Any.objects.all().order_by('-any1')
	res = [ [a.id, str(a) ] for a in annys ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


@permission_required_403('notes.posar_notes')
def inters(request):
	inters = InterAvaluacio.objects.all()
	res = [ [a.id, str(a) ] for a in inters ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


@permission_required_403('notes.posar_notes')
def grupsAny(request):
	interid = request.POST.get("inter")
	inter = InterAvaluacio.objects.get(id=interid)
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


	res = [ [a.id, str(a) ] for a in grups ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


@permission_required_403('notes.posar_notes')
def updateintergrup(request):
	gid = request.GET.get('gid')
	interid = request.GET.get('inter')
	checked = request.GET.get('checked')

	grup = Grup.objects.get(id=gid)
	inter = InterAvaluacio.objects.get(id=interid)

	if checked == 'true':
		inter.grups.add(grup)
	else:
		inter.grups.remove(grup)

	return HttpResponse()




@permission_required_403('notes.posar_notes')
def cursosinters(request):
	interid = request.GET.get("inter")
	inter = InterAvaluacio.objects.get(id=interid)
	grups = inter.grups.all()
	res = [ [a.id, str(a) ] for a in grups ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


@permission_required_403('notes.posar_notes')
def assignaturescursos(request):
	interid = request.POST.get("inter")
	inter = InterAvaluacio.objects.get(id=interid)
	grupid = request.POST.get("grup")
	grup = Grup.objects.get(id=grupid)
	assignatures = Assignatura.objects.all()

	for a in assignatures:
		try:
			AssignaturaGrupInter.objects.get(interavaluacio=inter, grup=grup, assignatura=a)
			a.checked = True
		except AssignaturaGrupInter.DoesNotExist:
			a.checked = False

	return render_to_response(
		'notes/assignaturescursos.html', {
		 	'grup': grup,
			'assignatures': assignatures,
		}
	)

@permission_required_403('notes.posar_notes')
def updateassignaturacurs(request):
	assid = request.GET.get('assid')
	interid = request.GET.get('inter')
	grupid = request.GET.get('grup')
	checked = request.GET.get('checked')

	assignatura = Assignatura.objects.get(id=assid)
	inter = InterAvaluacio.objects.get(id=interid)
	grup = Grup.objects.get(id=grupid)

	if checked == 'true':
		agi = AssignaturaGrupInter(interavaluacio=inter, grup=grup, assignatura=assignatura)
		agi.save()
	else:
		AssignaturaGrupInter.objects.filter(interavaluacio=inter, grup=grup, assignatura=assignatura).delete()

	return HttpResponse()


@permission_required_403('notes.posar_notes')
def comentari(request):
	pass



@permission_required_403('notes.posar_notes')
def nnota(request):
	fields = request.POST

	tipnota = TipNota.objects.get(id=fields['tnota'])
	alumne = Alumne.objects.get(id=fields['alumne'])
	assignatura = Assignatura.objects.get(id=fields['assignatura'])
	inter = InterAvaluacio.objects.get(id=fields['inter'])

	if dateInter(inter) == False:
		raise Exception("Date error")

	if fields['nota'] == "-1":
		Nota.objects.filter(tipnota=tipnota,alumne=alumne,assignatura=assignatura,interavaluacio=inter).delete()
		return HttpResponse()

	qualif = ItemNota.objects.get(id=fields['nota'])

	try:
		nota = Nota.objects.get(tipnota=tipnota,alumne=alumne,assignatura=assignatura,interavaluacio=inter)
		nota.nota = qualif
		nota.save()
	except:
		nota = Nota(
			nota = qualif,
			tipnota = tipnota,
			alumne = alumne,
			assignatura = assignatura,
			interavaluacio=inter,
		)
		nota.save()

	return HttpResponse()



@permission_required_403('notes.posar_notes')
def comentari(request):
	post = request.POST
	text = post['comentari']
	alumne = Alumne.objects.get(id=int(post['al']))
	assignatura = Assignatura.objects.get(id=int(post['as']))
	inter = InterAvaluacio.objects.get(id=int(post['inter']))

	if dateInter(inter) == False:
		raise Exception("Date error")

	if not re.match('^\s*$', text):
		try:
			com = Comentari.objects.get(alumne=alumne, assignatura=assignatura,interavaluacio=inter)
			com.text = text
			com.save()
		except:
			com = Comentari(
				text = text,
				alumne = alumne,
				assignatura = assignatura,
				interavaluacio=inter,
			)
			com.save()
	else:
		try:
			Comentari.objects.filter(alumne=alumne, assignatura=assignatura, interavaluacio=inter).delete()
		except:
			pass

	return HttpResponse()

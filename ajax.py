# -*- coding: utf-8 -*-

from functools import wraps

from django.contrib.auth.decorators import login_required, permission_required

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.decorators import available_attrs
from django.forms.models import model_to_dict

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from notes.models import *
from gestib.models import *

import re, datetime


#
# Torna una resposta de tipus application/json amb les dades que es passen com a paràmetre
#
def toJson(data):
    return HttpResponse(simplejson.dumps(data), content_type="application/json");


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


def getSubmateriesGrup(grup, inter):
    result = []
    for s in grup.submateries.all():
        result.append({ 'nom': s.descripcio, 'id': s.id })

    print grup, "Result: ", result
    return result


#
# Torna la interavaluacio activa
# I els cursos corresponents
#
@permission_required_403('notes.posar_notes')
def interCursos(request):
	# TODO: marcar interavaluació activa d'alguna manera...
	iact = Config.objects.all()[0].interactiva
	grups = iact.grups.all()
	theGrups = []
	for g in grups:
		gg = model_to_dict(g)
		assigs = []
		for a in getSubmateriesGrup(g, iact):
			assigs.append(a)
		gg['assignatures'] = assigs
		gg['nomcomplet'] = g.curs.nom + ' ' + g.nom
		theGrups.append(gg)


	return toJson({
		'id': iact.id,
		'nom': iact.nom,
		'data1': str(iact.data1),
		'data2': str(iact.data2),
		'any': str(iact.anny),
		'anyid': iact.anny.id,
		'grups': theGrups,
	})


#
# Alumnes d'un grup, en JSON
#
@permission_required_403('notes.posar_notes')
def alumnes(request, gid, anyid):
	grup = Grup.objects.get(id=gid)
	anny = Any.objects.get(id=anyid)
	als = []
	for m in Matricula.objects.filter(grup=grup,anny=anny):
		als.append(m.alumne)

	als = sorted(als, key=lambda al: al.llinatge1)
	return toJson([model_to_dict(a) for a in als])



#
# Items, en JSON
#
@permission_required_403('notes.posar_notes')
def itemsAlumne(request, interid, alid, assigid, gid):
	assignatura = Assignatura.objects.get(id=assigid)
	grup = Grup.objects.get(id=gid)
	inter = InterAvaluacio.objects.get(id=interid)
	alumne = Alumne.objects.get(id=alid)

	try:
		comentari = Comentari.objects.get(alumne=alumne,assignatura=assignatura,interavaluacio=inter).text
	except Comentari.DoesNotExist:
		comentari = ''

	tipnotes = TipNota.objects.all().order_by('ordre')

	notes = []
	for t in tipnotes:
		n = Nota.objects.filter(assignatura=assignatura,alumne=alumne,tipnota=t,interavaluacio=inter)
		nota = None
		if n:
			nota = model_to_dict(n[0])

		its = [model_to_dict(i) for i in ItemNota.objects.filter(grupNota=t.grupNota) ]
		notes.append({ 'tipnota': model_to_dict(t), 'nota': nota, 'its': its })

	desactivat = False
	dt = datetime.datetime.now().date()
	if dt < inter.data1 or dt > inter.data2:
		desactivat = True

	return toJson({
		'comentari': comentari,
		'desactivat': desactivat,
		'notes': notes,
	})



#
# Post on venen les notes d'una assignatura d'un alumne d'una INTER
#
# TODO: abans d'introduir la nota, verificar que estem en el periode corresponent...
@permission_required_403('notes.posar_notes')
def postNotes(request):
    if request.POST:
        mypost = simplejson.loads(request.body)
        # print mypost

        # TODO: sanitize
        inter = InterAvaluacio.objects.get(id=mypost['inter'])
        alumne = Alumne.objects.get(id=mypost['alumne'])
        assignatura = Assignatura.objects.get(id=mypost['assignatura'])

        # Comentari: Esborrem els existents i posem el nou
        comentari = mypost['comentari']
        coms = Comentari.objects.filter(alumne=alumne, assignatura=assignatura, interavaluacio=inter)
        if coms:
            coms.delete()

        if not re.match('^\s*$', comentari):
            com = Comentari(alumne=alumne, assignatura=assignatura, interavaluacio=inter, text=comentari)
            com.save()

        # Bucle que emmagatzema les notes dins la base de dades
        for n in mypost['notes']:
            tipnota = TipNota.objects.get(id=n['tipnota'])

            # Primer, esborrem les notes existents per aquella assignatura de l'alumne i inter
            nexistents = Nota.objects.filter(tipnota=tipnota, alumne=alumne, assignatura=assignatura, interavaluacio=inter)
            if nexistents:
                nexistents.delete()

            # Si hi ha nota, l'enregistrem
            if 'nota' in n.keys():
                if n['nota'] is not None:
                    itemNota = ItemNota.objects.get(id=n['nota'])
                    nn = Nota(tipnota=tipnota, alumne=alumne, assignatura=assignatura, interavaluacio=inter, nota=itemNota)
                    nn.save()

    return HttpResponse()










@permission_required_403('notes.posar_notes')
def inters(request):
    result = []
    annys = Any.objects.all().order_by('-any1')
    for a in annys:
        inters = InterAvaluacio.objects.filter(anny=a).order_by('-data1')
        result.append({ 'id': a.id, 'nom': str(a), 'inters': [
            {'nom': i.nom, 'id': i.id } for i in inters
        ] })

    return toJson(result)



#
# Retorna els anys ordenats de major a menor, en JSON
#
# @permission_required_403('notes.posar_notes')
# def anys(request):
# 	annys = Any.objects.all().order_by('-any1')
# 	res = [ [a.id, str(a) ] for a in annys ]
# 	return HttpResponse(simplejson.dumps(res), mimetype='application/json')
#

#
# # Retorna totes les interavaluacions, en format JSON. Les més recents primer
# #
# @permission_required_403('notes.posar_notes')
# def inters(request):
# 	inters = InterAvaluacio.objects.all().order_by('-data1')
# 	res = [ [a.id, str(a) ] for a in inters ]
# 	return HttpResponse(simplejson.dumps(res), mimetype='application/json')
#

#
# Retorna totes les interavaluacions d'un any (passat per post)
#
# @permission_required_403('notes.posar_notes')
# def intersAny(request, any_id):
# 	anny = Any.objects.get(id=any_id);
# 	inters = InterAvaluacio.objects.filter(anny=anny).order_by('-data1')
# 	res = [ [a.id, a.nom ] for a in inters ]
# 	return HttpResponse(simplejson.dumps(res), mimetype='application/json')
#
#








#
# Torna els grups de la interavaluació, en format JSON
#
@permission_required_403('notes.posar_notes')
def grupsInter(request, inter_id):
	inter = InterAvaluacio.objects.get(id=inter_id)
	ginter = inter.grups.all()

	res = [ [a.id, str(a) ] for a in ginter ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')




@permission_required_403('notes.posar_notes')
def updateintergrup(request):
	if request.method == 'POST':
		gid = request.POST.get('gid')
		interid = request.POST.get('inter')
		checked = request.POST.get('checked')

		grup = Grup.objects.get(id=gid)
		inter = InterAvaluacio.objects.get(id=interid)

		if checked == 'true':
			inter.grups.add(grup)
		else:
			inter.grups.remove(grup)

		return HttpResponse()


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
	if request.method == 'POST':
		assid = request.POST.get('assid')
		interid = request.POST.get('inter')
		grupid = request.POST.get('grup')
		checked = request.POST.get('checked')

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

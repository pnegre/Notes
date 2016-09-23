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

import aux


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
# Torna les submatèries d'un grup
#
def getSubmateriesGrup(grup, inter):
    result = []
    for s in grup.submateries.all():
        result.append({ 'nom': aux.beautifySubmateriaName(s.descripcio), 'id': s.id })

    return result

#
# Funció auxiliar, donada una inter, torna els grups
#
def GrupsFromInter(inter):
    grups = inter.grups.all()
    theGrups = []
    for g in grups:
        gg = model_to_dict(g)
        assigs = []
        for a in getSubmateriesGrup(g, inter):
        	assigs.append(a)
        gg['assignatures'] = assigs
        gg['nomcomplet'] = g.curs.nom + ' ' + g.nom
        theGrups.append(gg)

    return theGrups


#
# Torna la interavaluacio activa
# I els cursos corresponents
#
@permission_required_403('notes.posar_notes')
def interActivaCursos(request):
	# TODO: marcar interavaluació activa d'alguna manera...
	iact = Config.objects.all()[0].interactiva
	grups = GrupsFromInter(iact)

	return toJson({
		'id': iact.id,
		'nom': iact.nom,
		'data1': str(iact.data1),
		'data2': str(iact.data2),
		'any': str(iact.anny),
		'anyid': iact.anny.id,
		'grups': grups,
	})

#
# Torna els grups d'una interavaluació
#
@permission_required_403('notes.posar_notes')
def interCursos(request, interid):
    inter = InterAvaluacio.objects.get(id=interid)
    return toJson(GrupsFromInter(inter))


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
# Torna les notes i els comentaris d'un alumne a una assignatura a una inter, en JSON
#
@permission_required_403('notes.posar_notes')
def itemsAlumne(request, interid, alid, assigid, gid):
	assignatura = Submateria.objects.get(id=assigid)
	grup = Grup.objects.get(id=gid)
	inter = InterAvaluacio.objects.get(id=interid)
	alumne = Alumne.objects.get(id=alid)

	try:
		comentari = Comentari.objects.get(alumne=alumne,submateria=assignatura,interavaluacio=inter).text
	except Comentari.DoesNotExist:
		comentari = ''

	tipnotes = inter.tipnotes.all().order_by('ordre')

	notes = []
	for t in tipnotes:
		n = Nota.objects.filter(submateria=assignatura,alumne=alumne,tipnota=t,interavaluacio=inter)
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
        assignatura = Submateria.objects.get(id=mypost['assignatura'])

        # Comentari: Esborrem els existents i posem el nou
        comentari = mypost['comentari']
        coms = Comentari.objects.filter(alumne=alumne, submateria=assignatura, interavaluacio=inter)
        if coms:
            coms.delete()

        if not re.match('^\s*$', comentari):
            com = Comentari(alumne=alumne, submateria=assignatura, interavaluacio=inter, text=comentari)
            com.save()

        # Bucle que emmagatzema les notes dins la base de dades
        for n in mypost['notes']:
            tipnota = TipNota.objects.get(id=n['tipnota'])

            # Primer, esborrem les notes existents per aquella assignatura de l'alumne i inter
            nexistents = Nota.objects.filter(tipnota=tipnota, alumne=alumne, submateria=assignatura, interavaluacio=inter)
            if nexistents:
                nexistents.delete()

            # Si hi ha nota, l'enregistrem
            if 'nota' in n.keys():
                if n['nota'] is not None:
                    itemNota = ItemNota.objects.get(id=n['nota'])
                    nn = Nota(tipnota=tipnota, alumne=alumne, submateria=assignatura, interavaluacio=inter, nota=itemNota)
                    nn.save()

    return HttpResponse()



#
# Torna una llista amb les interavaluacions (anys i interavaluacions)
#
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
# Torna els grups de la interavaluació, en format JSON
#
@permission_required_403('notes.posar_notes')
def grupsInter(request, inter_id):
    inter = InterAvaluacio.objects.get(id=inter_id)
    ginter = inter.grups.all()
    grups = Grup.objects.filter(curs__anny=inter.anny)
    result = []
    for g in grups:
        checked = g in ginter
        result.append({'nom': str(g), 'id': g.id, 'checked': checked})

    return toJson(result)

#
# Assigna submatèries (assignatures) a una interavaluació
#
@permission_required_403('notes.posar_notes')
def saveInter(request):
    if request.method == 'POST':
        # Necessari perquè json no envia la info correctament codificada per django
        # TODO: sanitize data
        mypost = simplejson.loads(request.body)
        inter = InterAvaluacio.objects.get(id=mypost['inter'])
        inter.grups.clear()
        for c in mypost['cursos']:
            g = Grup.objects.get(id=c['id'])
            if c['checked']:
                inter.grups.add(g)

        return HttpResponse()

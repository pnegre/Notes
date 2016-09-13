# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('',

	# Vistes normals
	(r'^$', 'notes.views.llistat_cursos'),
	(r'^admin$', 'notes.views.admin'),
	(r'^admin2$', 'notes.views.admin2'),
	(r'^cursos$', 'notes.views.llistat_cursos'),
	# (r'^assignatura/(?P<inter_id>\d+)/(?P<as_id>\d+)/(?P<gr_id>\d+)$', 'notes.views.assig'),
	(r'^butlleti/(?P<inter_id>\d+)/(?P<grup_id>\d+)', 'notes.views.butlleti'),
	(r'^butlletins$', 'notes.views.butlletins2'),
	(r'^grupsany/(?P<inter_id>\d+)$', 'notes.views.grupsAny'),
	# (r'^butlletins_individuals$', 'notes.views.butlletins_individuals'),


	# AJAX
	# (r'^noucomentari$', 'notes.ajax.comentari'),
	# (r'^nnota$', 'notes.ajax.nnota'),
	(r'^grupsinter/(?P<inter_id>\d+)$', 'notes.ajax.grupsInter'),
	(r'^updateintergrup/$', 'notes.ajax.updateintergrup'),
	(r'^anys$', 'notes.ajax.anys'),
	(r'^inters$', 'notes.ajax.inters'),
	(r'^intersany/(?P<any_id>\d+)$', 'notes.ajax.intersAny'),
	(r'^assignaturescursos/$', 'notes.ajax.assignaturescursos'),
	(r'^updateassignaturacurs/$', 'notes.ajax.updateassignaturacurs'),



	# Nous
	(r'^interCursos$', 'notes.ajax.interCursos'),
	(r'^alumnes/(?P<gid>\d+)/(?P<anyid>\d+)$', 'notes.ajax.alumnes'),
	(r'^itemsAlumne/(?P<interid>\d+)/(?P<alid>\d+)/(?P<assigid>\d+)/(?P<gid>\d+)$', 'notes.ajax.itemsAlumne'),
	(r'^postNotes$', 'notes.ajax.postNotes'),
	# (r'^cursosinter/$', 'notes.ajax.cursosinters'),
	# (r'^getnotes/(?P<grup_id>\d+)/(?P<as_id>\d+)', 'notes.ajax.getnotes'),
	# (r'^llista_alumnes/(?P<curs_id>\d+)', 'notes.ajax.llista_alumnes'),

)

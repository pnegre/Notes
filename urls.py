# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	# Vistes normals
	(r'^admin$', 'notes.views.admin'),
	(r'^admin2$', 'notes.views.admin2'),
	(r'^$', 'notes.views.llistat_cursos'),
	(r'^cursos$', 'notes.views.llistat_cursos'),
	(r'^assignatura/(?P<inter_id>\d+)/(?P<as_id>\d+)/(?P<gr_id>\d+)$', 'notes.views.assig'),
	(r'^butlleti/(?P<inter_id>\d+)/(?P<grup_id>\d+)', 'notes.views.butlleti'),
	(r'^butlletins$', 'notes.views.butlletins2'),
	# (r'^butlletins_individuals$', 'notes.views.butlletins_individuals'),
	#

	# AJAX
	(r'^noucomentari$', 'notes.ajax.comentari'),
	(r'^nnota$', 'notes.ajax.nnota'),
	(r'^grupsany/$', 'notes.ajax.grupsAny'),
	(r'^grupsinter/$', 'notes.ajax.grupsInter'),
	(r'^updateintergrup/$', 'notes.ajax.updateintergrup'),
	# (r'^getnotes/(?P<grup_id>\d+)/(?P<as_id>\d+)', 'notes.ajax.getnotes'),
	# (r'^llista_alumnes/(?P<curs_id>\d+)', 'notes.ajax.llista_alumnes'),
	(r'^anys$', 'notes.ajax.anys'),
	(r'^inters$', 'notes.ajax.inters'),
	# (r'^cursosinter/$', 'notes.ajax.cursosinters'),
	(r'^assignaturescursos/$', 'notes.ajax.assignaturescursos'),
	(r'^updateassignaturacurs/$', 'notes.ajax.updateassignaturacurs'),


)

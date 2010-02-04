# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^curs/(?P<curs_id>\d+)$', 'notes.views.curs'),
	(r'^assignatura/(?P<as_id>\d+)$', 'notes.views.assig'),
	
	(r'^butlleti/(?P<curs_id>\d+)', 'notes.views.butlleti'),
	
	(r'^butlletins$', 'notes.views.butlletins2'),
	
	(r'^butlletins_individuals$', 'notes.views.butlletins_individuals'),
	
	
	(r'^noucomentari$', 'notes.ajax.comentari'),
	(r'^nnota/(?P<al_id>\d+)/(?P<as_id>\d+)/(?P<it_id>\d+)/(?P<tn_id>\d+)$', 'notes.ajax.nnota'),
	(r'^getnotes/(?P<curs_id>\d+)/(?P<as_id>\d+)', 'notes.ajax.getnotes'),
	(r'^llista_alumnes/(?P<curs_id>\d+)', 'notes.ajax.llista_alumnes'),
	
	
	(r'^upload$', 'notes.views.upload'),
	
	
	
	(r'^$', 'notes.views.llistat_cursos'),

)

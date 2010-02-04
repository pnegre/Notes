# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^curs/(?P<curs_id>\d+)$', 'notes.views.curs'),
	(r'^assignatura/(?P<as_id>\d+)$', 'notes.views.assig'),
	
	(r'^nnota/(?P<al_id>\d+)/(?P<as_id>\d+)/(?P<it_id>\d+)/(?P<tn_id>\d+)$', 'notes.views.nnota'),
	(r'^getnotes/(?P<curs_id>\d+)/(?P<as_id>\d+)', 'notes.views.getnotes'),
	
	(r'^butlleti/(?P<curs_id>\d+)', 'notes.views.butlleti'),
	
	(r'^butlletins$', 'notes.views.butlletins2'),
	(r'^llista_alumnes/(?P<curs_id>\d+)', 'notes.views.llista_alumnes'),
	(r'^butlletins_individuals$', 'notes.views.butlletins_individuals'),
	
	
	(r'^noucomentari$', 'notes.views.comentari'),
	
	(r'^upload$', 'notes.views.upload'),
	
	
	
	(r'^$', 'notes.views.llistat_cursos'),

)

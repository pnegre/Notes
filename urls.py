# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^curs/(?P<curs_id>\d+)$', 'notes.views.curs'),
	(r'^nnota/(?P<al_id>\d+)/(?P<as_id>\d+)/(?P<it_id>\d+)/(?P<tn_id>\d+)$', 'notes.views.nnota'),
	(r'^getnotes/(?P<curs_id>\d+)', 'notes.views.getnotes'),
	
	(r'^butlleti/(?P<curs_id>\d+)', 'notes.views.butlleti'),
	
	(r'^$', 'notes.views.llistat_cursos'),

)

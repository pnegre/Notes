# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('',

	# Vistes normals
	(r'^$', 'notes.views.llistat_cursos'),
	(r'^cursos$', 'notes.views.llistat_cursos'),
	(r'^butlletiPDF/(?P<inter_id>\d+)/(?P<grup_id>\d+)', 'notes.views.butlletiPDF'),
	(r'^butlletins$', 'notes.views.butlletins2'),
	(r'^adminInter$', 'notes.views.adminInter'),
	(r'^editSubmats$', 'notes.views.editSubsView'),


	# AJAX
	(r'^interActivaCursos$', 'notes.ajax.interActivaCursos'),
	(r'^interCursos/(?P<interid>\d+)$', 'notes.ajax.interCursos'),
	(r'^alumnes/(?P<gid>\d+)/(?P<anyid>\d+)$', 'notes.ajax.alumnes'),
	(r'^itemsAlumne/(?P<interid>\d+)/(?P<alid>\d+)/(?P<assigid>\d+)/(?P<gid>\d+)$', 'notes.ajax.itemsAlumne'),
	(r'^postNotes$', 'notes.ajax.postNotes'),
	(r'^inters$', 'notes.ajax.inters'),
	(r'^grupsInter/(?P<inter_id>\d+)$', 'notes.ajax.grupsInter'),
	(r'^tipnotesInter/(?P<interid>\d+)$', 'notes.ajax.tipnotesInter'),
	(r'^saveInter$', 'notes.ajax.saveInter'),

	(r'^submatsInter/(?P<interid>\d+)/(?P<gid>\d+)$', 'notes.ajax.submatsInter'),
	(r'^submatsPost$', 'notes.ajax.submatsPost'),

)

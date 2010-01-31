# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors


from notes.models import *

def curs(request,curs_id):
	curs = Curs.objects.filter(id=curs_id)[0]
	
	if request.method == "POST":
		fields = request.POST
		if 'newal' in fields.keys():
			al = Alumne(nom=fields['al'], l1=fields['l1'], l2=fields['l2'], curs=curs)
			al.save()
		elif 'newass' in fields.keys():
			ass = Assignatura(nom=fields['ass'], curs=curs)
			ass.save()
	
	asgs = Assignatura.objects.filter(curs=curs)
	als = Alumne.objects.filter(curs=curs).order_by('l1')
	tipnotes = TipNota.objects.all()
	items = ItemNota.objects
	notes = Nota.objects
	
	ntip=0
	for i in tipnotes:
		ntip += 1
					
	return render_to_response(
			'notes/curs.html', { 
				'curs': curs,
				'asgs': asgs,
				'alumnes': als,
				'tipnotes': tipnotes,
				'items': items,
				#'notes': notes,
				'ntip': ntip,
	} )


def assig(request,as_id):
	assignatura = Assignatura.objects.filter(id=as_id)[0]
	curs = Curs.objects.filter(assignatura=assignatura)[0]
	tipnotes = TipNota.objects.all()
	als = Alumne.objects.filter(curs=curs).order_by('l1')
	
	for a in als:
		c = Comentari.objects.filter(alumne=a,assignatura=assignatura)
		if (c):
			a.comm = c[0].text
		else:
			a.comm = ''
	
	return render_to_response(
			'notes/assignatura.html', { 
				'curs': curs,
				'assignatura': assignatura,
				'alumnes': als,
				'tipnotes': tipnotes,
	} )


def comentari(request):
	post = request.POST
	com = Comentari(
		text = post['comentari'],
		alumne = Alumne.objects.filter(id=int(post['al']))[0],
		assignatura = Assignatura.objects.filter(id=int(post['as']))[0]
	)
	com.save()
	return HttpResponse()



def nnota(request,al_id,as_id,it_id,tn_id):
	tipnota = TipNota.objects.filter(id=tn_id)[0]
	alumne = Alumne.objects.filter(id=al_id)[0]
	assignatura = Assignatura.objects.filter(id=as_id)[0]
	qualif = ItemNota.objects.filter(id=it_id)[0]
	try:
		nota = Nota.objects.filter(tipnota=tipnota,alumne=alumne,assignatura=assignatura)[0]
		nota.nota = qualif
		nota.save()
	except:
		nota = Nota(
			nota = qualif,
			tipnota = tipnota,
			alumne = alumne,
			assignatura = assignatura
		)
		nota.save()
		
	return HttpResponse()


def llistat_cursos(request):
	cursos = Curs.objects.all()
	return render_to_response(
			'notes/index.html', { 
				'cursos': cursos,
	} )
	


def getnotes(request,curs_id):
	notes = Nota.objects.filter(id=curs_id)
	curs = Curs.objects.filter(id=curs_id)
	r = {}
	als = Alumne.objects.filter(curs=curs)
	asgs = Assignatura.objects.filter(curs=curs)
	tipnotes = TipNota.objects.all()
	for a in als:
		r1 = {}
		for asg in asgs:
			r2 = {}
			for t in tipnotes:
				try:
					n = Nota.objects.filter(assignatura=asg,alumne=a,tipnota=t)[0]
					r2[t.id] = n.nota.id
				except:
					r2[t.id] = None
			r1[asg.id] = r2
		r[a.id] = r1
		
	return HttpResponse(simplejson.dumps( r ), mimetype='application/javascript')




from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait 

def butlleti(request,curs_id):
	curs = Curs.objects.filter(id=curs_id)
	als = Alumne.objects.filter(curs=curs).order_by('l1')
	asgs = Assignatura.objects.filter(curs=curs)
	tipnotes = TipNota.objects.all()
	
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

	# Our container for 'Flowable' objects
	elements = []
	
	# A large collection of style sheets pre-made for us
	styles = getSampleStyleSheet()
	
	# A basic document for us to write to 'rl_hello_platypus.pdf'
	doc = SimpleDocTemplate(response)
	doc.pagesize = landscape(A4)
	
	styles['Normal'].fontsize=8
	
	for al in als:
		# Create two 'Paragraph' Flowables and add them to our 'elements'
		elements.append(Paragraph("Es Liceu.<br/>Carrer Cabana, 31.<br/> 07141, Pont d'Inca, Marratxí<br/>E-MAIL: escola@esliceu.com<br/>Telèfon: 971 60 09 86<br/><br/><br/>",
			styles['Normal']))
		elements.append(Paragraph("Notes per " + str(al), styles['Heading1']))
		
		elements.append(Paragraph("<br/><br/>", styles['Normal']))
		
		
		kkk = []
		for a in asgs:
			nts = []
			nts.append(a.nom)
			for t in tipnotes:
				try:
					n = Nota.objects.filter(assignatura=a,alumne=al,tipnota=t)[0]
					nts.append(n.nota.it)
				except:
					nts.append("BLANK")
			kkk.append(nts)

		
		tits = [Paragraph(t.nom,styles['Normal']) for t in tipnotes ]
		tits.insert(0,'')
				
		data = []
		data.append(tits)
		for i in kkk:
			data.append(i)
	
		ts = [
			#('ALIGN', (1,1), (-1,-1), 'CENTER'),
			('GRID', (0,0), (-1,-1), 1, colors.black),
		]
		
		# Create the table with the necessary style, and add it to the
		# elements list.
		table = Table(data,style=ts)
		elements.append(table)
		
		comentaris = Comentari.objects.filter(alumne=al)
		for c in comentaris:
			elements.append(Paragraph("Comentaris de " + c.assignatura.nom, styles['Heading3']))
			elements.append(Paragraph(c.text, styles['Normal']))
		
		elements.append(PageBreak()) 
		
	
	# Write the document to disk
	doc.build(elements)
	return response
		
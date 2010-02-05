# -*- coding: utf-8 -*-

from django.http import HttpResponse

from notes.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors

import datetime

from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait


def butlletins_per_curs_i_alumne(curs,alumnes):
	assignatures = Assignatura.objects.filter(curs=curs)
	tipnotes = TipNota.objects.all().order_by('ordre')
	
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=butlletins' + str(curs) + '.pdf'
	
	# Our container for 'Flowable' objects
	elements = []
	
	# A large collection of style sheets pre-made for us
	styles = getSampleStyleSheet()
	
	# A basic document for us to write to 'rl_hello_platypus.pdf'
	doc = SimpleDocTemplate(response, leftMargin=25, rightMargin=25, topMargin=25, bottomMargin=25)
	doc.pagesize = landscape(A4)
	
	styles['Normal'].fontsize=8
	today = datetime.date.today()
	strdate = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
	
	for al in alumnes:
		#im = Image("/tmp/image.jpg")
		#im.hAlign = 'RIGHT'
		##elements.append(im)
		
		par = Paragraph("<b>Es Liceu</b>. Carrer Cabana, 31. 07141, Pont d'Inca, Marratxí<br/>Telèfon: 971 60 09 86. E-MAIL: escola@esliceu.com<br/><br/>",
			styles['Normal'])
		
		elements.append(par)
		
		elements.append(Paragraph(str(al), styles['Heading1']))
		
		elements.append(Paragraph("Data: " + strdate, styles['Normal']))
		elements.append(Paragraph("Curs: " + curs.nom, styles['Normal']))
		elements.append(Paragraph("Tutor: " + curs.tutor + "<br/><br/>", styles['Normal']))
		
		kkk = []
		for a in assignatures:
			nts = []
			nts.append(a.nom)
			for t in tipnotes:
				try:
					n = Nota.objects.filter(assignatura=a,alumne=al,tipnota=t)[0]
					nts.append(n.nota.it)
				except:
					nts.append("")
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
		
		coms = ""
		comentaris = Comentari.objects.filter(alumne=al)
		for c in comentaris:
			coms += "<b>" + c.assignatura.nom + ":</b> " + c.text + "  "
		
		elements.append(Paragraph("<br/><br/>", styles['Normal']))
		elements.append(Paragraph(coms, styles['Normal']))
		
		al_nom = str(al)
		s = "<br/>__________________________________________________________________________________________________________________________________________________<br/>" + "Alumne: " + al_nom + ". Grup: " + str(curs) + ". Tutor: " + str(curs.tutor) + ". Segona Interav." + "<br/>Signatura del Pare/mare:"
		#s = "<br/>_________________________________________________________________________________________________________________________________________<br/>" + "Alumne: " + str(al) + ". Grup: " + curs.nom + ". Tutor: " + curs.tutor 
		al_nom = str(al)
		par2 = Paragraph(s, styles["Normal"])
		
		elements.append(par2)
		
		elements.append(PageBreak()) 
		
	
	# Write the document to disk
	doc.build(elements)
	return response
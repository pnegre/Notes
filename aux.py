# -*- coding: utf-8 -*-

from django.http import HttpResponse

from notes.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors

import re,datetime

from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait

def beautifySubmateriaName(name):
    m = re.match('(.*)-[A-Za-z0-9]*$', name)
    if m:
        name = m.group(1)

    m = re.match('(.*)\(.*\)$', name)
    if m:
        name = m.group(1)

    return name

def butlletins_per_grup_i_alumne(inter, submateries, grup, alumnes):
	tipnotes = inter.tipnotes.all().order_by('ordre')

	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=butlletins_' + str(grup) + '.pdf'

	# Our container for 'Flowable' objects
	elements = []

	# A large collection of style sheets pre-made for us
	styles = getSampleStyleSheet()

	# A basic document for us to write to 'rl_hello_platypus.pdf'
	doc = SimpleDocTemplate(response, leftMargin=25, rightMargin=25, topMargin=25, bottomMargin=25)
	doc.pagesize = landscape(A4)

	styles['Normal'].fontsize=6
	today = datetime.date.today()
	strdate = str(today.day) + "/" + str(today.month) + "/" + str(today.year)

	for al in alumnes:
		dadesTaula = []
		for a in submateries:
			notesFiltrades = Nota.objects.filter(submateria=a,alumne=al,interavaluacio=inter)
			if len(notesFiltrades) == 0: continue
			nts = []
			if not a.curta:
				# nts.append(Paragraph(beautifySubmateriaName(a.nom), styles["Normal"]))
				nts.append(beautifySubmateriaName(a.nom))
			else:
				# nts.append(Paragraph(beautifySubmateriaName(a.curta), styles["Normal"]))
				nts.append(beautifySubmateriaName(a.curta))

			for t in tipnotes:
				try:
					n = notesFiltrades.get(tipnota=t)
					# nts.append(Paragraph(n.nota.it, styles["Normal"]))
					nts.append(n.nota.it)
				except:
					nts.append("")
			dadesTaula.append(nts)

		if len(dadesTaula) == 0:
			continue

		internom = ""
		if inter.nomButlleti is not None:
			internom = unicode(inter.nomButlleti)
		if internom is None or internom == "":
			internom = unicode(inter.nom)
		internom += " %d-%d" % (inter.anny.any1, inter.anny.any2)

		par = Paragraph("<b>Es Liceu</b>. Carrer Cabana, 31. 07141, Pont d'Inca, Marratxí<br/>Telèfon: 971 60 09 86. E-MAIL: escola@esliceu.com<br/><br/>",
			styles['Normal'])
		elements.append(par)
		elements.append(Paragraph(internom, styles['Normal']))

		elements.append(Paragraph(unicode(al), styles['Heading1']))

		elements.append(Paragraph("Data: " + strdate, styles['Normal']))
		elements.append(Paragraph("Curs: " + unicode(grup), styles['Normal']))
		elements.append(Paragraph("Tutor/a: " + unicode(grup.tutor) + "<br/><br/>", styles['Normal']))

		tits = [Paragraph(t.nom,styles['Normal']) for t in tipnotes ]
		tits.insert(0,'')

		data = []
		data.append(tits)
		for i in dadesTaula:
			data.append(i)

		ts = [
			#('ALIGN', (1,1), (-1,-1), 'CENTER'),
			('GRID', (0,0), (-1,-1), 1, colors.black),
			('FONTSIZE', (0, 0), (-1, -1), 8),
		]

		# Create the table with the necessary style, and add it to the
		# elements list.
		table = Table(data,style=ts)
		elements.append(table)

		coms = ""
		comentaris = Comentari.objects.filter(alumne=al,interavaluacio=inter)
		for c in comentaris:
			coms += "<b>" + beautifySubmateriaName(c.submateria.nom) + ":</b> " + c.text + "  "

		elements.append(Paragraph("<br/><br/>", styles['Normal']))
		elements.append(Paragraph(coms, styles['Normal']))

		s = "<br/>" + "_" * 137 + "<br/>"
		s += "Alumne/a: " + unicode(al) + ". Grup: " + unicode(grup) + ". "
		s += internom + "<br/>"
		s += "Signatura del Pare/mare:"
		par2 = Paragraph(s, styles["Normal"])

		elements.append(par2)
		elements.append(PageBreak())

	# Build the pdf document
	doc.build(elements)
	return response

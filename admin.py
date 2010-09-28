# -*- coding: utf-8 -*-

from django.contrib import admin
from notes.models import *

admin.site.register(Assignatura)
admin.site.register(Nota)
admin.site.register(TipNota)
admin.site.register(ItemNota)
admin.site.register(Comentari)



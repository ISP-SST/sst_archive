from django.contrib import admin

from observations.models import Instrument


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	pass

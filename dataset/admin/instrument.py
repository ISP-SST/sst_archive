from django.contrib import admin

from dataset.models import Instrument


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	"""Admin class for the Instrument model"""
	pass

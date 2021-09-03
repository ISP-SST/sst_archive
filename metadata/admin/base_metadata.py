from django.contrib import admin

class BaseMetadataAdmin(admin.ModelAdmin):
	'''Base admin class for the metadata models'''
	date_hierarchy = 'date_beg'
	list_display = ['oid', 'date_beg']
	list_filter = []
	readonly_fields = []
	
	def get_readonly_fields(self, request, obj=None):
		'''Return a list or tuple of field names that will be displayed as read-only'''
		
		# Allow superuser to change everything
		# Allow regular user to set the oid once but not change it
		if request.user.is_superuser:
			return []
		elif obj is None:
			return super().get_readonly_fields(request, obj)
		else:
			return super().get_readonly_fields(request, obj) + ['oid']

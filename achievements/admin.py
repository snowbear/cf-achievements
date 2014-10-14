from django.contrib import admin
from achievements.models import Contest, Contestant, Achievement, Rewarding

class ContestAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'date')
	list_filter = ['date']
	search_fields = ['name']
	ordering = ['-date']

admin.site.register(Contest, ContestAdmin)
admin.site.register(Contestant)
admin.site.register(Achievement)
admin.site.register(Rewarding)

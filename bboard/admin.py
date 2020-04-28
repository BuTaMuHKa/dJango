from django.contrib import admin

from .models import Bd, Rubric

class BdAdmin(admin.ModelAdmin):
	list_display = ('title', 'content', 'price', 'published', 'rubric')
	list_display_links = ('title', 'content')
	search_fields = ('title', 'content',)

class RubricAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_display_links = ('name',)
	search_fields = ('name',)

admin.site.register(Bd, BdAdmin) 
admin.site.register(Rubric, RubricAdmin)
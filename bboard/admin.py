from django.contrib import admin

from .models import Bd, Rubric, Img


class BdAdmin(admin.ModelAdmin):
	# def img(self, img):
	# 	img = Img.objects.value(bd_id=Bd.pk)
	# 	return '<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.img)
	# def img_img(self):
	# if self.img:
	# 	return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.img.url))
	# else:
	# 	return '(изображение отсутствует)'

	list_display = ['title', 'price', 'content', 'published', 'rubric',]
	list_display_links = ('title', 'rubric', )
	list_editable = ('content',)
	search_fields = ('title', 'content',)

class RubricAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_display_links = ('name',)
	search_fields = ('name',)

class ImgAdmin(admin.ModelAdmin):
	list_display = ('img',)

admin.site.register(Bd, BdAdmin) 
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Img, ImgAdmin)
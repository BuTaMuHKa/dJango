from django.db import models
from datetime import datetime
from os.path import splitext

def get_timestamp_path(instance, filename):
	return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
	
#Дистпечер записей Рубрики
class RubricManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().order_by('name')
	def order_by_bd_count(self):
		return super().get_queryset().annotate(cnt=models.Count('bd')).order_by('-cnt')

#Диспетчер записи вторичной модели(Bd)
class BdManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().order_by('-published')

class Rubric(models.Model):
	name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'
		ordering = ['name']
	objects = RubricManager()

class Bd(models.Model):
	title = models.CharField(max_length=50, verbose_name='Товар')
	content = models.TextField(null=True, blank=True, verbose_name='Описание')
	price = models.FloatField(null=True, blank=True, default=0, verbose_name='Цена')
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
	photo = models.ImageField(verbose_name='фото', upload_to= get_timestamp_path)
	rubric = models.ForeignKey('Rubric', null=True,
		on_delete=models.PROTECT, verbose_name='Рубрика')
	
	class Meta:
		verbose_name_plural='Объявления'
		verbose_name='Объявление'
		ordering=['-published']
	objects = models.Manager()
	reverse = BdManager()

class Img(models.Model):
	img = models.ImageField(verbose_name='Изображение', upload_to = get_timestamp_path)
	bd = models.ForeignKey('Bd', null=True, on_delete=models.PROTECT, verbose_name='Фото')
	class Meta:
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'


class File(models.Model):
	file = models.FileField(verbose_name='Файл')
	desc = models.TextField(verbose_name='Описание')
	class Meta:
		verbose_name = 'Файл'
		verbose_name_plural = 'Файлы'

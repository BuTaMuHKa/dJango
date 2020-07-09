from django.db import models
from datetime import datetime
from os.path import splitext
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal
from django.utils.safestring import mark_safe

add_rubric = Signal(providing_args=['created','instance'])

def get_timestamp_path(instance, filename):
	return '%s%s%s' % ('archives/%Y/%m/%d/', datetime.now().timestamp(), splitext(filename)[1])

#Дополнение к модели User
# class Profile(models.Model):
# 	phone = models.CharField(max_length = 12, verbose_name = 'Номер телефона')
# 	user = models.OneToOneField(User, on_delete = models.CASCADE)

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

#Рубрика
class Rubric(models.Model):
	name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'
		ordering = ['name']
	objects = RubricManager()

#Посты 
class Bd(models.Model):
	title = models.CharField(max_length=50, verbose_name='Товар')
	content = models.TextField(null=True, blank=True, verbose_name='Описание')
	price = models.FloatField(null=True, blank=True, default=0, verbose_name='Цена')
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
	rubric = models.ForeignKey('Rubric', null=True,
		on_delete=models.CASCADE, verbose_name='Рубрика')
	class Meta:
		verbose_name_plural='Объявления'
		verbose_name='Объявление'
		ordering=['-published']
	objects = models.Manager()
	reverse = BdManager()

#Фото связанная с Bd как расширение изображений 
class Img(models.Model):
	class Meta:
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'
	img = models.ImageField(verbose_name='Изображение', null=False, help_text='150x150px', upload_to = 'archives/%Y/%m/%d/')
	bd = models.OneToOneField(Bd, on_delete=models.CASCADE)

#Файлы
class File(models.Model):
	file = models.FileField(verbose_name='Файл')
	desc = models.TextField(verbose_name='Описание')
	class Meta:
		verbose_name = 'Файл'
		verbose_name_plural = 'Файлы'


#Сигналы обрпботки данных
def post_save_dispatcher(sender, **kwargs):
	if kwargs['created']:
		#print(kwargs)
		print('Объявление в рубрике "%s" создано' % kwargs['instance'].rubric.name)
post_save.connect(post_save_dispatcher, sender=Bd)

def post_delete_dispatcher(sender, **kwargs):
	print('Запись "%s" была удалена' % kwargs['instance'].title)
post_delete.connect(post_delete_dispatcher, sender=Bd)

# def add_rubric_dispatcher(sender, **kwargs):
# 	if kwargs['created']:
# 		print('Добавлена рубрика "%s"' % kwargs['instance'])
# 		print(kwargs['instance'])
# add_rubric.connect(add_rubric_dispatcher, sender=Rubric)

from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.urls.base import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import edit, base, list, dates
from django.forms import modelformset_factory
from django.contrib import messages
from django.template import RequestContext
from django.dispatch import Signal
from django.core.mail import EmailMessage, get_connection, send_mail, get_connection,send_mass_mail
from django.template.loader import render_to_string
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.core.cache import cache
from precise_bbcode.bbcode import get_parser
from samplesite.settings import BASE_DIR
from datetime import datetime
import os

from .models import Bd, Rubric, Img, add_rubric
from .forms import BdForm, RegisterForm, SearchForm
CRITICAL = 50
FILES_ROOT = os.path.join(BASE_DIR, 'files')

#Главная страница с пагинаторомs
@vary_on_cookie
def index(request):
	rubrics = Rubric.objects.all()
	bds = Bd.objects.all()
	paginator = Paginator(bds, 10)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.page(page_num)
	searchf = SearchForm(request.POST)
	if 'last_connection' in request.COOKIES:
		visits = int(request.COOKIES['last_connection']) + 1
	else:
		visits = 1
	context = {'rubrics':rubrics, 'page': page, 'bds': page.object_list, 'form': searchf, 'visits':visits}
	response = HttpResponse(render(request, 'bboard/index.html', context))
	response.set_cookie('last_connection', visits)
	return response



# Изменение/добавление/удаление рубрики
def rubric(request):
	RubricFormSet = modelformset_factory(Rubric, fields=('name',),
		can_order=True, can_delete=True)
	if request.method == "POST":
		formset = RubricFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('bboard:index')
	else:
		formset = RubricFormSet()
		context = {'formset':formset}
		return render(request, 'bboard/rubrics.html', context)

# Удаление записи 
def delete(request, pk):
	rubrics = Rubric.objects.all()
	if request.user.is_superuser:
		bd = Bd.objects.get(pk=pk)
		if request.method == 'POST':
			bd.delete()
			return HttpResponseRedirect(reverse('bboard:by_rubric',
				kwargs={'rubric_id': bd.rubric.pk}))
		else:
			context = {'bd': bd, 'rubrics':rubrics}
			return render(request, 'bboard/bd_delete.html', context)
	else:
		return HttpResponseForbidden('У вас нет доступа к этой странице')

#Изменение записи с посредством формы связаной с моделью
def update(request, pk):
	rubrics = Rubric.objects.all()
	if request.user.is_superuser or request.user.is_staff:
		bd = Bd.objects.get(pk=pk)
		if request.method == 'POST':
			bdf = BdForm(request.POST, request.FILES, instance=bd)
			if bdf.is_valid():
				bdf.save()
				messages.add_message(request, messages.SUCCESS, 'Обявление измнено успешно', extra_tags='first second')
				return HttpResponseRedirect(reverse('bboard:by_rubric',
					kwargs={'rubric_id': bdf.cleaned_data['rubric'].pk}, ))
			else:
				context = {'form':bdf, 'rubrics':rubrics}
				return render(request, 'bboard/bd_update.html', context)
		else:
			bdf = BdForm(instance=bd)
			context = {'form':bdf, 'rubrics':rubrics}
			return render(request, 'bboard/bd_update.html', context)
	else:
		return HttpResponseForbidden('У вас нет доступа')

#Самописный контроллер для отдельной записи
def detail(request, pk):
	bd = Bd.objects.get(pk=pk)
	rubrics = Rubric.objects.all()
	
	# if 'last' in request.COOKIES:
	# 	visits = int(request.COOKIES['last']) + 1
	# else:
	# 	visits = 1 
	context = { 'bd':bd, 'rubrics':rubrics}
	# response = HttpResponse(render(request, 'bboard/bd_detail.html', context))
	# response.delete_cookie('last_connection')
	# response.set_cookie('last', visits)

	return render(request, 'bboard/bd_detail.html', context)

#Все рубрики
def by_rubric(request, rubric_id):
	bds = Bd.objects.filter(rubric=rubric_id)
	rubrics = Rubric.objects.order_by_bd_count()
	current_rubric = Rubric.objects.get(pk=rubric_id)
	context = {'bds': bds, 'rubrics': rubrics, 'current_rubric': current_rubric}
	return render(request, 'bboard/by_rubric.html', context)

#Сохрание записи в базе данных 
def add_and_save(request):
	rubrics = Rubric.objects.all()
	bd = Bd.objects.all()
	if request.user.is_authenticated:
		if request.method == 'POST':
			bdf = BdForm(request.POST, request.FILES)  
			if bdf.is_valid():
				bdf.save()
				return HttpResponseRedirect(reverse('bboard:by_rubric',
					kwargs={'rubric_id': bdf.cleaned_data['rubric'].pk}))
			else:
				contex = {'form':bdf, 'rubrics': rubrics}
				return render(request, 'bboard/create.html', contex)
		else:
			bdf = BdForm
			contex = {'form': bdf, 'rubrics': rubrics}
			return render(request, 'bboard/create.html', contex)
	else:
		return HttpResponseForbidden('У вас нет доступа')

#Регистрация пользователя
def registerUser(request):
	rubrics = Rubric.objects.all()
	form = RegisterForm(request.POST)
	if request.method == "POST":
		if form.is_valid():
			send_mail('Test', 'test!', 'webmaster@samplesite.ru', ['user@site.ru'], html_message='<h1>HEllo loshok</h1>')
			form.save()
			return HttpResponseRedirect(reverse('bboard:login'))
		else:
			contex = {'form': form, 'rubrics': rubrics}
			return render(request, 'registration/register_user.html', contex)
	else:
		contex = {'form': form, 'rubrics': rubrics}
		return render(request, 'registration/register_user.html', contex)

#Поисковая система
def search(request):
	if request.method == 'POST' or request.method == 'GET':
		sf = SearchForm(request.POST)
		if sf.is_valid():
			keyword = sf.cleaned_data['keyword']
			bds = Bd.objects.filter(title = keyword)
			context = {'bds': bds, 'form': sf}
			return render(request, 'bboard/search_result.html', context)
	else:
		sf = SearchForm()
		text = "Извините по вашему запросу ничего не найдено"
	context = {'form': sf, 'text': text } 
	return render(request, 'bboard/search.html', context)

#Вывод загружунных файлов
def showfiles(request):
	img = Img.objects.all()
	context = {'imgs': img}
	return render(request, 'bboard/files.html', context)

#Удаление фото
def deleteimg(request, pk):
	img = Img.objects.get(pk=pk)
	img.img.delete()
	img.delete()
	return redirect('bboard:index')

#Отправка сигнала в консоль при добавление рубрики 
add_rubric.send(Rubric, created = True, instance = rubric)

#Отправка электронного письма без вложений
# em = EmailMessage(subject = 'Test', body = 'Test', to = ['butajiuk6@gmail.com'])
# em.send()

#Отправка письма с вложеном пароле
# em = EmailMessage(subject='Ваш новый пароль',
# 	body = 'Ваш новый пароль находится во вложении',
# 	attachments = [('password.txt', '123456789', 'tex/plain')],
# 	to = ['butajiuk6@gmail.com'])
# em.send()

#Отправка электронной почты с вложение хранящийся на локальном диске
# em = EmailMessage(subject = 'Запрошеный вами файл', body = 'Сам файл', to = ['butajiuk6@gmail.com'])
# em.attach_file(r'C:\User\admin\desktop\file.txt')
# em.send()

#Отправка почты с помощью шаблона django
# context = {'user':'Вася Пупкин'}
# s = render_to_string('email/letter.txt', context)
# em = EmailMessage(subject = 'Оповещение', body = s, to = ['vpupkin@mail.ru'])
# em.send()

#Отправка множество писем с разовым подключением к серверу SMTP 
# cn = get_connection()
# cn.open()
# email1 = EmailMessage(..., connection=cn)
# email1.send()
# email2 = EmailMessage(..., connection=cn)
# email2.send()
# cn.close()

#Отправка перечь писем
# msg1 = send_mass_mail('Подписка','Потверждение подписки', 'admin@site.ru', ['user@site.ru'])
# msg2 = send_mass_mail('Одобрение', 'Ваша подписка потверждена', 'admin@site.ru', ['user@site.ru'])
# send_mass_mail(msg1, msg2)
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls.base import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import edit, base, list, dates
from django.forms import modelformset_factory
from precise_bbcode.bbcode import get_parser 

from .models import Bd, Rubric
from .forms import BdForm, RegisterForm, SearchForm

#Главная страница с пагинатором 
def index(request):
		rubrics = Rubric.objects.all()
		bds = Bd.objects.all()
		paginator = Paginator(bds, 5)
		if 'page' in request.GET:
			page_num = request.GET['page']
		else:
			page_num = 1
		page = paginator.page(page_num)
		contex = {'rubrics':rubrics, 'page': page, 'bds': page.object_list}
		return render(request, 'bboard/index.html', contex)

# Изменение рубрики
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
	if request.user.is_superuser:
		bd = Bd.objects.get(pk=pk)
		if request.method == 'POST':
			bd.delete()
			return HttpResponseRedirect(reverse('bboard:by_rubric',
				kwargs={'rubric_id': bd.rubric.pk}))
		else:
			context = {'bd': bd}
			return render(request, 'bboard/bd_delete.html', context)
	else:
		return HttpResponseForbidden('У вас нет доступа к этой странице')

#Изменение записи с посредством формы связаной с моделью
def update(request, pk):
	if request.user.is_superuser or request.user.is_staff:
		bd = Bd.objects.get(pk=pk)
		if request.method == 'POST':
			bdf = BdForm(request.POST, instance=bd)
			if bdf.is_valid():
				bdf.save()
				return HttpResponseRedirect(reverse('bboard:by_rubric',
					kwargs={'rubric_id': bdf.cleaned_data['rubric'].pk}))
			else:
				context = {'form':bdf}
				return render(request, 'bboard/bd_update.html', context)
		else:
			bdf = BdForm(instance=bd)
			context = {'form':bdf}
			return render(request, 'bboard/bd_update.html', context)
	else:
		return HttpResponseForbidden('У вас нет доступа')

#Самописный контроллер для отдельной записи
def detail(request, pk):
	parser = get_parser()
	bd = Bd.objects.get(pk=pk)
	parser_content = parser.render(bd.content)
	rubric = Rubric.objects.all()
	context = {'bd':bd, 'rubric':rubric}
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
	if request.user.is_superuser or request.user.is_staff:
		if request.method == 'POST':
			bdf = BdForm(request.POST)
			if bdf.is_valid():
				bdf.save()
				return HttpResponseRedirect(reverse('bboard:by_rubric',
				kwargs={'rubric_id': bdf.cleaned_data['rubric'].pk}))
			else:
				contex = {'form':bdf}
				return render(request, 'bboard/create.html', contex)
		else:
			bdf = BdForm
			contex = {'form': bdf}
			return render(request, 'bboard/create.html', contex)
	else:
		return HttpResponseForbidden('У вас нет доступа')
		
#Регистрация пользователя
def registerUser(request):
	form = RegisterForm(request.POST)
	if request.method == "POST":
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('bboard:login'))
		else:
			contex = {'form': form}
			return render(request, 'registration/register_user.html', contex)
	else:
		contex = {'form': form}
		return render(request, 'registration/register_user.html', contex)

def search(request):
	if request.method == 'POST':
		sf = SearchForm(request.POST)
		if sf.is_valide():
			keyword = sf.cleaned_data['keyword']
			rubric_id = sf.cleaned_data['rubric_id'].pk
			bds = Bd.objects.filter()
			context = {'bds': bds}
			return render(request, 'bboard/search_result.html', context)
	else:
		sf = SearchForm()
	context = {'form':sf} 
	return render(request, 'bboard/serch.html', context)

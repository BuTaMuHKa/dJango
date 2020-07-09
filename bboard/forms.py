from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms import modelform_factory, DecimalField, formset_factory
from django.forms.widgets import Select
from django.core.exceptions import ValidationError
#from captcha.fields import CaptchaField

from .models import Bd, Rubric, Img, File

# Форма связанная с моделю хранится в памяти и полезно для постоянного вызова формы
class BdForm(forms.ModelForm):
	#Валидация 
	# def clean(self):
	# 	super().clean()
	# 	errors = {}
	# 	if not self.content:
	# 		errors['content'] = ValidationError('Укажите описание товара')
	# 	if self.price < 0:
	# 		errors['price'] = ValidationError('Цена не может быть отрицательная')
	# 	elif errors:
	# 		raise ValidationError(errors)
	#Поля
	title = forms.CharField(label = 'Название товара')
	content = forms.CharField(label = 'Описание товара',
			# validators=[validators.RegexValidator(regex='^.{4,}$')],
			# error_messages={'invalid': 'Слишком короткое описание'},
			widget = forms.widgets.Textarea())
	price = forms.DecimalField(label = 'Цена', decimal_places=2)
	rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
			label = 'Рубрика', help_text = 'Не забудьте Рубрику')
	# photo = forms.ImageField(
	# 	label='Изображение',
	# 	# validators=[validators.FileExtensionValidator(
	# 	# allowed_extensions=('gif', 'jpg', 'png'))],
	# 	# error_messages={'invalid_extension':'Этот формат файлов'+\
	# 	# 	'не поддерживается'},
	# 	widget=forms.widgets.ClearableFileInput(attrs={'multiple':True}))

	
	#captcha = CaptchaField()
	class Meta:
		model = Bd
		fields = ('title', 'content', 'price', 'rubric')

#Форма для фото
class ImgForm(forms.ModelForm):
	img = forms.ImageField(
		label='Изображение',
		required=False,
		widget=forms.widgets.ClearableFileInput(attrs={'multiple':True}))

	class Meta:
		model = Img
		fields = ('img',) 

# Форма регистрации для пользователя(контролер и модель пока отсутсвует)
class RegisterForm(forms.ModelForm):
	username = forms.CharField(label='Ваше имя', required=True)
	email = forms.EmailField(label='Ваш почтовый адрес', required=True)
	password1 = forms.CharField(strip=False, label='Ваш пароль', required=True )
	password2 = forms.CharField(strip=False, label='Повторите пароль', required=True)
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

#Форма не связаная с моделью
class SearchForm(forms.Form):
	keyword = forms.CharField(max_length=20, required=False, error_messages=None)


# class ImgNotModelForm(forms.Form):
# 	img = forms.ImageField(
# 		label='Изображение',
# 		validators=[validators.FileExtensionValidator(
# 		allowed_extensions=('gif', 'jpg', 'png')
# 		)],
# 		error_messages={'invalid_extension':'Этот формат файлов'+\
# 		'не поддерживается'},
# 		widget=forms.widgets.ClearableFileInput(attrs={'multiple':True}))
# 	bd_id = forms.ModelChoiceField(
# 		queryset = Bd.objects.get(pk=later))	

class FileForm(forms.ModelForm):
	img = forms.FileField(
		label='Файл')
	desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
	class Meta:
		model = Img
		fields = '__all__'

#Фабрика формы не связаная с моделью
#fs = formset_factory(SearchForm, extra = 3, can_delete = True)
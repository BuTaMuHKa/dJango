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
	title = forms.CharField(label = 'Название товара')
	content = forms.CharField(label = 'Описание товара',
			# validators=[validators.RegexValidator(regex='^.{4,}$')],
			# error_messages={'invalid': 'Слишком короткое описание'},
			widget = forms.widgets.Textarea())
	price = forms.DecimalField(label = 'Цена', decimal_places=2)
	rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
			label = 'Рубрика', help_text = 'Не забудьте Рубрику')
	photo = forms.ImageField(
		label='Изображение',
		validators=[validators.FileExtensionValidator(
		allowed_extensions=('gif', 'jpg', 'png'))],
		error_messages={'invalid_extension':'Этот формат файлов'+\
			'не поддерживается'},
		widget=forms.widgets.ClearableFileInput(attrs={'multiple':True}))

	def clean(self):
		super().clean()
		errors = {}
		if not self.cleaned_data['content']:
			errors['content'] = ValidationError('Укажите описание товара')
		elif self.cleaned_data['price'] < 0:
			errors['price'] = ValidationError('Цена не может быть отрицательная')
		elif errors:
			raise ValidationError(errors)
	#captcha = CaptchaField()
	class Meta:
		model = Bd
		fields = ('title', 'content', 'price', 'rubric', 'photo')

# Форма регистрации для пользователя(контролер и модель пока отсутсвует)
class RegisterForm(forms.ModelForm):
	username = forms.CharField(label='Ваше имя', required=False)
	email = forms.EmailField(label='Ваш почтовый адрес', required=False )
	password1 = forms.CharField(strip=False, label='Ваш пароль', required=False )
	password2 = forms.CharField(strip=False, label='Повторите пароль', required=False)
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

#Форма не связаная с моделью
class SearchForm(forms.Form):
	keyword = forms.CharField(max_length=20, label='', error_messages={'required': ''})

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
fs = formset_factory(SearchForm, extra = 3, can_delete = True)
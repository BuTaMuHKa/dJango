from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms import modelform_factory, DecimalField, formset_factory
from django.forms.widgets import Select
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import Bd, Rubric

#Фабрика формы, она не хранится в памяти, хороша только тогда когда нужно вызвать редкую форму 
# BdForm = modelform_factory(Bd,
# 	fields = ('title', 'content', 'price', 'rubric'),
# 	labels = {'title':'Название товара'},
# 	help_texts = {'rubric':'Не забудьте рубрику'},
# 	field_classes = {'price': DecimalField},
# 	widgets = {'rubric': Select(attrs={'size':5})})

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
	def clean(self):
		super().clean()
		errors = {}
		if not self.cleaned_data['content']:
			errors['content'] = ValidationError('Укажите описание товара')
		elif self.cleaned_data['price'] < 0:
			errors['price'] = ValidationError('Цена не может быть отрицательная')
		elif errors:
			raise ValidationError(errors)
	captcha = CaptchaField()
	class Meta:
		model = Bd
		fields = ('title', 'content', 'price', 'rubric')

# Форма связанная с моделю при котором c быстрыми полями формы похож на 1 способ
# class BdForm (ModelForm):
# 	class Meta:
# 		model = ВЬ
# 		fields = ('title', 'content', 'price', 'rubric')
# 		labels = {'title': 'Название товара!'}
# 		help_texts = {'rubric': 'Не забудьте задать рубрику!'}
# 		field_classes = {'price': DecirnalField}
# 		widgets = {'rubric': Select(attrs= { 'size' : 8})}

# Форма регистрации для пользователя(контролер и модель пока отсутсвует)
class RegisterForm(UserCreationForm):
	email = forms.EmailField(label='Ваш почтовый адрес')
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

# class AuthenticationUserForm(forms.ModelForm):
# 	login = forms.CharField(label='Логин')
# 	password = forms.CharField(label='Пароль')
# 	class Meta:
# 		model = User
# 		fields = ('login', 'password')

#Форма не связаная с моделью
class SearchForm(forms.Form):
	keyword = forms.CharField(max_length=20, label='Искаемое слово')
	rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')

#Фабрика формы не связаная с моделью
fs = formset_factory(SearchForm, extra = 3, can_delete = True)
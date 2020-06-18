from django.urls import path, reverse_lazy
from django.contrib import admin
from django.contrib.auth.views import ( LoginView,LogoutView,
	PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
	PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from .views import (add_and_save, update, detail,
	by_rubric, index, delete, rubric, registerUser, showfiles, search, deleteimg)

app_name = 'bboard'
urlpatterns = [
	#path('deleteimg/<int:pk>/', deleteimg, name="deleteimg"),
	#path('test_cookie/', test_cookie, name='test_cookie'),
	path('search/', search, name='search'),
	path('showfiles/', showfiles, name='showfiles'),
	path('add/', add_and_save,
		name='add'),
	path('update/<int:pk>/', update,
		name='update'),
	path('delete/<int:pk>/', delete,
		name='delete'),
	path('rub_delete/', rubric,
		name='rub_delete'),
	path('detail/<int:pk>/', detail,
		name='detail'),
	path('<int:rubric_id>/', by_rubric,
		name='by_rubric'),
	path('accounts/login/', LoginView.as_view(),
		name='login'),
	path('accounts/logout/', LogoutView.as_view(
		next_page='bboard:index'),
		name='logout'),
	path('accounts/password_change/', PasswordChangeView.as_view(
		success_url=(reverse_lazy('bboard:password_change_done')),
		template_name='registration/change_password.html'),
		name='password_change'),
	path('accounts/password_change/done/', PasswordChangeDoneView.as_view(),
		name='password_change_done'),
	path('accounts/password_reset/', PasswordResetView.as_view(
		success_url=(reverse_lazy('bboard:password_reset_done')),
		template_name='registration/reset_password.html',
		subject_template_name='registration/reset_subject.txt',
		email_template_name='registration/reset_email.html'),
		name='password_reset'),
	path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
		template_name='registration/email_sent.html'),
		name='password_reset_done'),
	path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
		success_url=(reverse_lazy('bboard:password_reset_complete')),
		template_name='registration/confirm_password.html'),
		name='password_reset_confirm'),
	path('accounts/reset/done/', PasswordResetCompleteView.as_view(
		template_name='registration/password_confirmed.html'),
		name='password_reset_complete'),
	path('register_user/', registerUser,
		name='register'),
	path('', index, name='index'),
]
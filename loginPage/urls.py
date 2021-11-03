from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('loginError/', views.loginError, name='loginError'),
    path('loginSuccess/', views.loginSuccess, name='loginSuccess'),
    path('checkInput/', views.checkInput, name='checkInput'),
]

# An attempt was made to use parameters for path(), but was unsuccessful.
# These are code bits that may be used for the implementation later
# path('login/<valid>/', views.login, name='login'),
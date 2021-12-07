from django.urls import path

from . import views
from polls.views import IndexView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPath, name='login'),
    path('loginError/', views.loginError, name='loginError'),
    path('createUser/', views.createUser, name='createUser'),
    path('createUserError/', views.createUserError, name='createUserError'),
    path('checkLogin/', views.checkLogin, name='checkLogin'),
    path('checkUser/', views.checkUser, name='checkUser'),
    path('loginHelp/', views.loginHelp, name='loginHelp'),
    path('checkLogin/', views.checkLogin, name='checkLogin'),
    path('logoutPage/', views.logoutPage, name='logoutPage'),
    path('polls/', IndexView.as_view(), name='polls')
]

# An attempt was made to use parameters for path(), but was unsuccessful.
# These are code bits that may be used for the implementation later
# path('login/<valid>/', views.login, name='login'),
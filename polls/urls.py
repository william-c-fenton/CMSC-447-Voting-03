from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('CreateQuestion/', views.create_question, name='create-question'),
    path('<int:pk>/CreateChoice/', views.create_choice, name='create-choice'),
    path('voteSuccessful/', views.voteSuccessful, name='voteSuccessful'),
]
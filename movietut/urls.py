from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-movies/', views.MovieListView.as_view(), name='all-movies'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
]

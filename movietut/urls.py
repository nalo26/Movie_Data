from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-movies/', views.MovieListView.as_view(), name='all-movies'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('signup/', views.MemberCreationView.as_view(), name='signup'),
    path('search/', views.search_movie, name='search-movie'),
    path('profile/', views.profile, name='profile'),

]



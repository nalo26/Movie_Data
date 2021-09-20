from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('signup/', views.MemberCreationView.as_view(), name='signup'),
]



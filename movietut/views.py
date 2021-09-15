from django.views.generic import ListView, DetailView
from .models import Movie


class MovieListView(ListView):
    model = Movie
    paginate_by = 30


class MovieDetailView(DetailView):
    model = Movie

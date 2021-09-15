from django.views.generic import ListView
from .models import Movie


class MovieListView(ListView):
    model = Movie
    paginate_by = 30

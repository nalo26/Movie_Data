from datetime import time, timedelta
from django.views.generic import ListView, DetailView
from .models import Movie
from django.shortcuts import render
from django.utils import timezone

def index(request):
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=14)
    movies_to_be_released = Movie.objects.filter(release_date__range=[start_date + timedelta(days=1), end_date]).order_by("release_date")
    movies_recently_released= Movie.objects.filter(release_date__range=[start_date - timedelta(days=14), start_date]).order_by("-release_date")
    context = {
        "movies_to_be_released": movies_to_be_released,
        "movies_recently_released": movies_recently_released,
    }
    return render(request, "movietut/index.html", context)

class MovieListView(ListView):
    model = Movie
    paginate_by = 30


class MovieDetailView(DetailView):
    model = Movie

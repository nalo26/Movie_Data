from datetime import time
from django.views.generic import ListView, DetailView
from .models import Movie
from django.shortcuts import render
from django.utils import timezone

def index(request):
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=14)
    movies_to_be_released = Movie.objects.filter(release_date__range=[start_date, end_date])
    context = {
        "movies_to_be_released": movies_to_be_released,
        "movies": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 
    }
    return render(request, "movietut/index.html", context)

class MovieListView(ListView):
    model = Movie
    paginate_by = 30


class MovieDetailView(DetailView):
    model = Movie

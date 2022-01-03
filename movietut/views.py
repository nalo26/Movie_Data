from django.utils import timezone
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
import json

from .forms import MovieForm, MemberCreationForm
from .models import Movie, Member, Genre


def index(request):
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=14)
    movies_to_be_released = Movie.objects.filter(release_date__range=[start_date + timedelta(days=1), end_date]).order_by("release_date")
    movies_recently_released= Movie.objects.filter(release_date__range=[start_date - timedelta(days=14), start_date]).order_by("-release_date")
    movies_recently_released = list(movies_recently_released)
    movies_top_rated= Movie.objects.filter(popularity__gt=80.0).order_by("popularity")

  
    genres = list(request.user.genres.all())



    context = {
        "movies_to_be_released": movies_to_be_released,
        "movies_recently_released": movies_recently_released,
        "movies_top_rated": movies_top_rated,
        "genres" : genres,
    }

    # if request.user.is_authenticated:
    r_movies = getRecommendedMovies()
    context["movies_recommended"] = r_movies
            
    return render(request, "movietut/index.html", context)

def getRecommendedMovies():
    try:
        with open("recommended_movies.json", 'r') as f:
            movies = json.load(f)
        return [Movie.objects.get(id=i) for i in movies]

    except Exception: return []


class MovieListView(ListView):
    model = Movie
    paginate_by = 30


class MovieDetailView(DetailView):
    model = Movie

    def post(self, request, *args, **kwargs):
        user_movies = request.user.movies
        if self.get_object() in user_movies:
            movie = user_movies.get(pk=self.get_object().pk)
        else:
            movie = user_movies.create(pk=self.get_object().pk)
        action = request.POST.get('ajax-action')
        if action == 'ajax-like':
            movie.is_liked = True
        elif action == 'ajax-bookmark':
            movie.is_wanted = True
        elif action == 'ajax-grade':
            movie.mark = 5
        movie.save()

        if not movie.is_liked and not movie.is_wanted and movie.mark is None:
            user_movies.remove(movie)

        return JsonResponse({'action_result': f'Action: {action}, movie: {self.get_object().title}!'})


class MemberCreationView(CreateView):
    form_class = MemberCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def search_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.cleaned_data['movie']
            return redirect(reverse_lazy('movie-detail', kwargs={
                'pk': movie.pk
            }))
    else:
        return redirect(reverse_lazy('index'))

    context = {
        'form': form
    }

    return render(request, 'movietut/base.html', context)


def profile(request):
    if request.method == 'POST':
        genre = Genre.objects.get(pk=request.POST.get('genre_pk'))
        genre_action = request.POST.get('genre_action')
        result = 'added'
        if genre_action == 'genre_add':
            request.user.genres.add(genre)
        else:
            result = 'deleted'
            request.user.genres.remove(genre)

        return JsonResponse({'action_result': result})

    genres = {genre: False for genre in Genre.objects.all()}
    for genre in genres:
        for genre_user in request.user.genres.all():
            if genre_user == genre:
                genres[genre] = True
    
    context = {
        "genres" : genres,
    }

    return render(request, 'movietut/profile.html', context)


from django.utils import timezone
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .forms import MovieForm, MemberCreationForm
from .models import Movie, Member


def index(request):
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=14)
    movies_to_be_released = Movie.objects.filter(release_date__range=[start_date + timedelta(days=1), end_date]).order_by("release_date")
    movies_recently_released= Movie.objects.filter(release_date__range=[start_date - timedelta(days=14), start_date]).order_by("-release_date")
    movies_top_rated= Movie.objects.filter(popularity__gt=80.0).order_by("popularity")

    context = {
        "movies_to_be_released": movies_to_be_released,
        "movies_recently_released": movies_recently_released,
        "movies_top_rated": movies_top_rated,
    }

    if request.user.is_authenticated:
        context["movies_recommended"] = get_users_recommendations()
            
    return render(request, "movietut/index.html", context)


def get_users_recommendations():
    return None


class MovieListView(ListView):
    model = Movie
    paginate_by = 30


class MovieDetailView(DetailView):
    model = Movie

    def post(self, request, *args, **kwargs):
        action = request.POST.get('ajax-action')
        if action == 'ajax-list':
            pass
        elif action == 'ajax-like':
            pass
        elif action == 'ajax-bookmark':
            pass
        elif action == 'ajax-grade':
            pass
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

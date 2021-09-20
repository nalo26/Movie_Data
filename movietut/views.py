from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .forms import MovieForm
from .models import Movie


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

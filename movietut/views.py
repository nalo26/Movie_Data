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


def search_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            piece = form.cleaned_data['piece']
            return redirect(reverse_lazy('movie-detail', kwargs={
                'pk': piece.pk
            }))
    else:
        return redirect(reverse_lazy('index'))

    context = {
        'form': form
    }

    return render(request, 'movietut/base.html', context)

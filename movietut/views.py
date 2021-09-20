from django.views.generic import ListView, DetailView
from .models import Movie
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import MemberCreationForm


class MovieListView(ListView):
    model = Movie
    paginate_by = 30


class MovieDetailView(DetailView):
    model = Movie

class MemberCreationView(CreateView):
    form_class = MemberCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

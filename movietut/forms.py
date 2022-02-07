from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django_select2 import forms as s2forms
from functools import reduce
from unidecode import unidecode
from .models import Movie, Member


class MovieWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "title__icontains",
    ]

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        search_fields = self.get_search_fields()
        select = Q()
        term = term.replace('\t', ' ')
        term = term.replace('\n', ' ')
        term = unidecode(term)
        for t in [t for t in term.split(' ') if not t == '']:
            select &= reduce(lambda x, y: x | Q(**{y: t}), search_fields,
                             Q(**{search_fields[0]: t}))
        if dependent_fields:
            select &= Q(**dependent_fields)

        return queryset.filter(select).distinct()


class MovieForm(forms.Form):
    movie = forms.ModelChoiceField(
        widget=MovieWidget(attrs={
                'data-width': '100%',
                'data-placeholder': 'Rechercher un film...',
                'data-allow-clear': 'true',
            },
        ),
        queryset=Movie.objects.all()
    )
    

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username', 'last_name', 'first_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


from .forms import MovieForm


def inject_form(request):
    return {
        'form': MovieForm()
    }

from django.shortcuts import render


def vue1(request):
    return render(request, template_name='movietut/index.html', context={'nom': 'Jacques'})

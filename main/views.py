from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'main/landing.html')


def store(request):
    return render(request, 'main/store.html')

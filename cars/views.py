from django.http import HttpResponse
from django.shortcuts import render
from .models import Car

def index(request):
    cars = Car.objects.all()[:10]
    return render(request, "cars/homePage.html", {'cars': cars})

def load(request):
        if request.method == 'GET':
            _id = int(request.GET['_id'])
            n = _id + 10
            cars = Car.objects.all()[_id:n]
            return render(request, "cars/reload.html", {'cars': cars})

        else:
            return HttpResponse("Request method is not a GET")
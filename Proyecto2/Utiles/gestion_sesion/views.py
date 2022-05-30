from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
# def home(request):
#     return HttpResponse("Bienvenido al Sistema SmileSoft")
def home(request):
    return render (request, 'index.html')

def iniciosesion (request):
    return render (request, 'iniciosesion.html')


def inicio (request):
    return render (request, 'inicio.html')

def cierre (request):
    pass
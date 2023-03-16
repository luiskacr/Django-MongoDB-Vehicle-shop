from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

#Esta funcion me esta dando un error al renderizar el archivo signup en django
def home(request):
    return render(request, 'home.html')
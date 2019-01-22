from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context = {'boldmessage':'crunchy,creamy,cookie,candy,cupcake!'}
    return render(request,'rango/index.html',context=context)

def about(request):
    context = {'yourname':'Richard Nemeth'}
    return render(request,'rango/about.html',context=context)

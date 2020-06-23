from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import ModelCode


# Create your views here.
def index(request):
    return HttpResponse("Hello World.")

def access_code(request):
    codes = ModelCode.objects.all()
    context = {'codes':codes}
    return HttpResponse(render(request, 'scrap/modelcode.html',context))

def addcode(request):
    code = request.GET.get('code','')
    year = request.GET.get('year','')
    make = request.GET.get('make','')
    model = request.GET.get('model','')
    
    new_code = ModelCode(code=code,year=year,make=make,model=model)
    new_code.save()

    return HttpResponse()
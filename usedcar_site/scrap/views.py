from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
import json
import os
from .models import ModelCode, Record


# Create your views here.
def index(request):
    return HttpResponse("Hello World.")

def access_code(request):
    # pylint: disable=no-member
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
    
    return redirect('access_code')

def deletecode(request):
    code = request.GET.get('code','')
    # pylint: disable=no-member
    new_code = ModelCode.objects.get(code=code)
    new_code.delete()
    
    return redirect('access_code')

def importdb(request):
    path = os.path.join(os.path.split(os.getcwd())[0], 'usedcar','usedcar.json')
    with open(path) as f:
        data = json.load(f)
        for i in data:
            new_record = Record(text=i['text'], model=i['model'], zip_code=i['zip'], price=i['price'].replace(',', ''), mileage=i['mileage'].replace(',', ''))
            new_record.save()

    return HttpResponse('Imported.')
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
import json
import os
from .ny_demo import ny_demo


# Create your views here.
def index(request):
    return HttpResponse(ny_demo())
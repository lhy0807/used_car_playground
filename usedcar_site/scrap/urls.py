from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('modelcode',views.ModelCode,name='code'),
    path('addcode',views.addcode,name='addcode'),
]
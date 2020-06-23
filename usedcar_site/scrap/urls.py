from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('modelcode',views.access_code,name='access_code'),
    path('addcode/',views.addcode,name='addcode'),
    path('deletecode/',views.deletecode,name='deletecode'),
    path('importdb/',views.importdb,name='importdb'),
]
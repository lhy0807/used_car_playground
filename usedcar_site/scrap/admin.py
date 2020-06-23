from django.contrib import admin
from .models import ModelCode
# Register your models here.

class CodeAdmin(admin.ModelAdmin):
    fields = ['code','year','make','model']

admin.site.register(ModelCode, CodeAdmin)
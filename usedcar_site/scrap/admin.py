from django.contrib import admin
from .models import ModelCode, Record
# Register your models here.

class CodeAdmin(admin.ModelAdmin):
    fields = ['code','year','make','model']

class RecordAdmin(admin.ModelAdmin):
    fields = ['id','text','model','zip_code','price','mileage']

admin.site.register(ModelCode, CodeAdmin)
admin.site.register(Record, RecordAdmin)
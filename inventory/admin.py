from django.contrib import admin
from inventory.models import atten,work
# Register your models here.

@admin.register(atten)
class AttenAdmin(admin.ModelAdmin):
    list_display=['id','day','mudeem','najim','nijam']
    
@admin.register(work)
class WorkAdmin(admin.ModelAdmin):
    list_display=['number','name','quantity','price']
    
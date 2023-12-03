from django.contrib import admin
from .models import Record,Carbrand,Cartypes,Vehicle

# Register your models here.
admin.site.register(Record)
admin.site.register(Carbrand)
admin.site.register(Cartypes)
admin.site.register(Vehicle)
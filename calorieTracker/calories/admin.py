from django.contrib import admin

# Register your models here.

from .models import Food,Consume, Profile
admin.site.register(Food)
admin.site.register(Consume)
admin.site.register(Profile)

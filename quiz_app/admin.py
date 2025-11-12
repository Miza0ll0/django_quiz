from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Theme, Question

admin.site.register(Theme)
admin.site.register(Question)

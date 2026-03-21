from django.contrib import admin
from .models import *

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    ordering = ('id',)

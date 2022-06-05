from django.contrib import admin
from .models import ToDo

class ToDoAdmin(admin.ModelAdmin):
    list_display = ['task', 'is_complete']
admin.site.register(ToDo, ToDoAdmin)
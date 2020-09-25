from django.contrib import admin

# Register your models here.

from main_app.models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)

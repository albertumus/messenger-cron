from django.contrib import admin
from .models import Message, Date, WeekDay

admin.site.register(Message)
admin.site.register(Date)
admin.site.register(WeekDay)
from django.contrib import admin
from .models import User, GameRecord, DetailRecord


admin.site.register(User)
admin.site.register(GameRecord)
admin.site.register(DetailRecord)
# Register your models here.


from django.contrib import admin
from .models import User, GameRecord, DetailRecord, Renew


admin.site.register(User)
admin.site.register(GameRecord)
admin.site.register(DetailRecord)
admin.site.register(Renew)
# Register your models here.


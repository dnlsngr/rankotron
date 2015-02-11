from django.contrib import admin
from leagues.models import League, Team, Week, Position

# Register your models here.
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Week)
admin.site.register(Position)
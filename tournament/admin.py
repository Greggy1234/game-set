from django.contrib import admin
from .models import Matches, Tournament

# Register your models here.
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tour',
        'location',
        'start_date',
        'end_date',
        'series',
        'court',
        'surface',
    )

class MatchesAdmin(admin.ModelAdmin):
    list_display = (
        'tournament',
        'round',
        'winner',
        'loser',
    )

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Matches, MatchesAdmin)
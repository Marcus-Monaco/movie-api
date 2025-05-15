from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'directors', 'genre', 'rating', 'has_poster', 'created_at')
    search_fields = ('title', 'directors', 'genre', 'plot')
    list_filter = ('year', 'genre', 'rating', 'created_at')
    readonly_fields = ('poster_url',)
    
    def has_poster(self, obj):
        return bool(obj.poster)
    has_poster.boolean = True
    has_poster.short_description = 'Poster'

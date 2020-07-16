"""
common contexts goes here, registerd at settings.py
"""

from .models import Genre

def genres(request):
    all_genre = Genre.objects.all()
    return {'all_genres': all_genre}

import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    """
    Filtros para o modelo Movie.
    """
    # Filtro para rating (permite filtrar por intervalo)
    rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    
    # Filtro para título (permite busca parcial, case-insensitive)
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    # Filtro para gênero (permite busca parcial, case-insensitive)
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='icontains')
    
    # Filtro para ano
    year = django_filters.NumberFilter(field_name='year')
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    
    class Meta:
        model = Movie
        fields = ['title', 'year', 'genre', 'rating', 'directors']

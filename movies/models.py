from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .services import get_movie_data

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    directors = models.CharField(max_length=255, null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    rating = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)  # Para armazenar a URL do poster da OMDb API
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Se for um novo objeto (sem ID) ou se o título foi alterado e os campos estão vazios
        if not self.pk or (self._state.adding is False and (
            not self.year or not self.directors or not self.genre or not self.plot or not self.poster_url
        )):
            # Busca dados do filme na OMDb API
            movie_data = get_movie_data(self.title)
            
            if movie_data:
                # Atualiza os campos com os dados da API
                if 'Year' in movie_data and not self.year:
                    try:
                        self.year = int(movie_data['Year'])
                    except (ValueError, TypeError):
                        pass
                
                if 'Director' in movie_data and not self.directors:
                    self.directors = movie_data['Director']
                
                if 'Genre' in movie_data and not self.genre:
                    self.genre = movie_data['Genre']
                
                if 'Plot' in movie_data and not self.plot:
                    self.plot = movie_data['Plot']
                
                if 'imdbRating' in movie_data and not self.rating:
                    try:
                        self.rating = float(movie_data['imdbRating'])
                    except (ValueError, TypeError):
                        pass
                
                # Adiciona a URL do poster
                if 'Poster' in movie_data and movie_data['Poster'] != 'N/A' and not self.poster_url:
                    self.poster_url = movie_data['Poster']
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.core.files.base import ContentFile
from .models import Movie
from .serializers import MovieSerializer
from .filters import MovieFilter

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar e editar filmes.
    
    Fornece as ações padrão 'list', 'create', 'retrieve', 'update' e 'destroy'.
    """
    queryset = Movie.objects.all().order_by('-created_at')
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    filterset_class = MovieFilter
    
    @action(detail=True, methods=['post'])
    def download_poster(self, request, pk=None):
        """
        Action personalizada para fazer download do poster da URL e salvar como arquivo.
        """
        movie = self.get_object()
        
        if not movie.poster_url:
            return Response(
                {"error": "Este filme não possui URL de poster."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if movie.poster:
            return Response(
                {"error": "Este filme já possui um poster carregado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Faz o download da imagem
            response = requests.get(movie.poster_url)
            if response.status_code != 200:
                return Response(
                    {"error": "Não foi possível baixar o poster."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Extrai o nome do arquivo da URL
            filename = movie.poster_url.split('/')[-1]
            if not filename:
                filename = f"{movie.title.replace(' ', '_')}_poster.jpg"
            
            # Salva o conteúdo como um arquivo
            movie.poster.save(filename, ContentFile(response.content), save=True)
            
            return Response(
                {"success": "Poster baixado com sucesso.", "poster": movie.poster.url},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao baixar o poster: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

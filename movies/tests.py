from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie
from unittest.mock import patch

class MovieAPITests(APITestCase):
    """
    Testes para a API de filmes.
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria alguns filmes para usar nos testes.
        """
        # Cria filmes diretamente no banco de dados para testes
        self.movie1 = Movie.objects.create(
            title="The Shawshank Redemption",
            year=1994,
            directors="Frank Darabont",
            genre="Drama",
            plot="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            rating=9.3
        )
        
        self.movie2 = Movie.objects.create(
            title="The Godfather",
            year=1972,
            directors="Francis Ford Coppola",
            genre="Crime, Drama",
            plot="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            rating=9.2
        )
        
        # URL para listar/criar filmes
        self.list_url = reverse('movie-list')
    
    @patch('movies.services.get_movie_data')
    def test_create_movie_with_auto_fields(self, mock_get_movie_data):
        """
        Testa a criação de um filme com apenas o título e verifica se
        os campos foram preenchidos automaticamente.
        """
        # URL do poster para o mock
        poster_url = 'https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_SX300.jpg'
        
        # Configura o mock para retornar dados fictícios
        mock_get_movie_data.return_value = {
            'Year': '1999',
            'Director': 'Lana Wachowski, Lilly Wachowski',
            'Genre': 'Action, Sci-Fi',
            'Plot': 'When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.',
            'imdbRating': '8.7',
            'Poster': poster_url
        }
        
        # Dados para criar um novo filme
        data = {'title': 'The Matrix'}
        
        # Faz a requisição POST para criar o filme
        response = self.client.post(self.list_url, data, format='json')
        
        # Verifica se a criação foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o filme foi criado com os dados corretos
        self.assertEqual(Movie.objects.count(), 3)  # 2 do setUp + 1 novo
        
        # Obtém o filme criado
        created_movie = Movie.objects.get(title='The Matrix')
        
        # Verifica se os campos foram preenchidos automaticamente
        self.assertEqual(created_movie.year, 1999)
        self.assertEqual(created_movie.directors, 'Lana Wachowski, Lilly Wachowski')
        self.assertEqual(created_movie.genre, 'Action, Sci-Fi')
        self.assertEqual(created_movie.plot, 'When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.')
        self.assertEqual(created_movie.rating, 8.7)
        self.assertEqual(created_movie.poster_url, poster_url)  # Usando a mesma URL do mock
    
    def test_list_movies(self):
        """
        Testa a listagem de todos os filmes.
        """
        # Faz a requisição GET para listar os filmes
        response = self.client.get(self.list_url)
        
        # Verifica se a listagem foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a resposta contém a estrutura de paginação
        self.assertIn('results', response.data)
        
        # Verifica se retornou o número correto de filmes
        self.assertEqual(len(response.data['results']), 2)
        
        # Verifica se os filmes estão na ordem correta (mais recente primeiro)
        self.assertEqual(response.data['results'][0]['title'], self.movie2.title)
        self.assertEqual(response.data['results'][1]['title'], self.movie1.title)
    
    def test_retrieve_movie(self):
        """
        Testa a busca de um filme pelo ID.
        """
        # URL para buscar o filme pelo ID
        detail_url = reverse('movie-detail', args=[self.movie1.id])
        
        # Faz a requisição GET para buscar o filme
        response = self.client.get(detail_url)
        
        # Verifica se a busca foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se os dados do filme estão corretos
        self.assertEqual(response.data['title'], self.movie1.title)
        self.assertEqual(response.data['year'], self.movie1.year)
        self.assertEqual(response.data['directors'], self.movie1.directors)
        self.assertEqual(response.data['genre'], self.movie1.genre)
        self.assertEqual(response.data['plot'], self.movie1.plot)
        self.assertEqual(response.data['rating'], self.movie1.rating)

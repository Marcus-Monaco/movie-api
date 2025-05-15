import requests
from decouple import config

def get_movie_data(title):
    """
    Faz uma requisição HTTP para a OMDb API com o título do filme
    e retorna os dados do filme.
    
    Args:
        title (str): O título do filme a ser consultado
        
    Returns:
        dict: Um dicionário contendo os dados do filme ou None se não encontrado
    """
    api_key = config('OMDB_API_KEY')
    
    if not api_key:
        raise ValueError("OMDB_API_KEY não encontrada nas variáveis de ambiente")
    
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('Response') == 'True':
            # Retorna os dados relevantes do filme
            return {
                'Year': data.get('Year'),
                'Director': data.get('Director'),
                'Genre': data.get('Genre'),
                'Plot': data.get('Plot'),
                'imdbRating': data.get('imdbRating'),
                'Poster': data.get('Poster')  
            }
        return None
    except Exception as e:
        print(f"Erro ao consultar a OMDb API: {e}")
        return None

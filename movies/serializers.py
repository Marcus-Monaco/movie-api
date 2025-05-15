from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # Serializa todos os campos do modelo
        read_only_fields = ['poster_url']  # Campos de leitura apenas
    
    def validate_title(self, value):
        """
        Valida que o título não pode ser vazio.
        """
        if not value.strip():
            raise serializers.ValidationError("O título não pode ser vazio.")
        return value

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet

# Cria um router e registra nosso ViewSet
router = DefaultRouter()
router.register(r'movies', MovieViewSet)

# As URLs da API são determinadas automaticamente pelo router
urlpatterns = [
    path('', include(router.urls)),
]

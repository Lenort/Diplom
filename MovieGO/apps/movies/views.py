from django.db import models
from django.shortcuts import render
from requests import request
from rest_framework import  permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
import sqlite3
from .models import Movie, Actor, Review
from django.shortcuts import render


from rest_framework.response import Response as DRF_Response
from rest_framework.request import Request as DRF_Request
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip, MovieFilter, PaginationMovies


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class RecomendViewSet(viewsets.ViewSet):

    def get_queryset(self):
        recomend = Movie.objects.filter

        return recomend
        
   

class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


def index(request):
    movies = Movie.objects.all()
    

    sqlite_connection = sqlite3.connect('db.sqlite3')
    cur = sqlite_connection.cursor()
    one_result = cur.execute("""SELECT title, avg(value) FROM movies_movie  JOIN movies_rating ON movies_movie.id  =  movies_rating.ratings_id JOIN movies_ratingstar ON movies_rating.star_id = movies_ratingstar.id  GROUP BY movies_movie.id HAVING avg(value) > 1.0 LIMIT 5""").fetchall()
    print(one_result)
    data = {"recomend":one_result}
    return render(request, 'movies/index.html',{'movies':movies})




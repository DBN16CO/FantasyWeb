from django.urls import path

from . import views

urlpatterns = [
    path('<int:league_id>/', views.get_league_standings, name='league_details')]

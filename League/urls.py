from django.urls import path

from . import views

urlpatterns = [
    path('<int:league_id>/', views.get_league_standings, name='league_standings'),
    path('<int:league_id>/my_team', views.get_league_my_team, name="league_my_team"),
    path('<int:league_id>/schedule', views.get_league_schedule, name="league_schedule"),
    path('<int:league_id>/free_agents', views.get_league_free_agents, name="league_free_agents"),
    path('<int:league_id>/trade_block', views.get_league_trade_block, name="league_trade_block"),
    path('<int:league_id>/draft', views.get_league_draft, name="league_draft"),
    path('<int:league_id>/forums', views.get_league_forums, name="league_forums"),
    path('<int:league_id>/settings', views.get_league_settings, name="league_settings"),
    path('<int:league_id>/commish_settings', views.get_league_commish_settings, name="league_commish_settings")
]

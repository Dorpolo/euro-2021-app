import django.contrib.auth.urls
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView().get, name='home'),
    path('add-your-prediction-group-stage/', views.AddBetsView.as_view(), name='add_your_bet'),
    path('add-your-prediction-group-stage/edit/<int:pk>', views.UpdateBetView.as_view(), name='update_your_bet'),
    path('create-league/', views.CreateLeagueView.as_view(), name='create_league'),
    path('join-a-league/', views.CreateLeagueMemberView.as_view(), name='create_league_member'),
    path('league-terms/', views.TermsView.as_view(), name='terms'),
    path('add-your-image/', views.UserImageView.as_view(), name='add_image'),
    path('match-predictions/', views.AllPredictionsView.as_view(), name='predictions' ),
    path('league-table/', views.LeagueTableView.as_view(), name='league_table'),
    path('update-league-member/edit/<int:pk>', views.UpdateLeagueMember.as_view(), name='update_league_member'),
    path('numbers-next-match/', views.GameStatsView.next, name='next_match_stats'),
    path('numbers-last-match/', views.GameStatsView.prev, name='prev_match_stats'),
    path('top-players/', views.plot_top_players, name='top_players'),
    path('my-predictions/', views.MyPredictionsView.as_view(), name='my_predictions'),
    path('live-match-next/', views.LiveGameView.next, name='live_next_match'),
    path('live-match-prev/', views.LiveGameView.prev, name='live_prev_match'),
]


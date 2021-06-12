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
    path('match-predictions/', views.ScoreView.as_view(), name='predictions'),
    path('league-table/', views.LeagueTableView.as_view(), name='league_table'),
    path('update-league-member/edit/<int:pk>', views.UpdateLeagueMember.as_view(), name='update_league_member'),
    path('numbers-next-match/', views.plot_index, name='next_match_stats'),
    path('numbers-last-match/', views.plot_index_last_match, name='prev_match_stats'),
]


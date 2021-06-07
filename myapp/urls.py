import django.contrib.auth.urls
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView().get, name='home'),
    path('add_your_bet/', views.AddBetsView.as_view(), name='add_your_bet'),
    path('add_your_bet/edit/<int:pk>', views.UpdateBetView.as_view(), name='update_your_bet'),
    path('create_league/', views.CreateLeagueView.as_view(), name='create_league'),
    path('create_user/', views.CreateLeagueMemberView.as_view(), name='create_league_member'),
    path('score_predictions/<int:pk>', views.predictions, name='predictions'),
    path('stats/', views.index, name='stats'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('add_your_image/', views.UserImageView.as_view(), name='add_image'),
    path('predictions/', views.ScoreView.as_view(), name='predictions'),
]


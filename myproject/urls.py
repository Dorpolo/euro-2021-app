import django.contrib.auth.urls
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView().get, name='home'),
    path('admin/', admin.site.urls),
    path('add_your_bet/', views.AddBetsView.as_view(), name='add_your_bet'),
    path('add_your_bet/edit/<int:pk>', views.UpdateBetView.as_view(), name='update_your_bet'),
    path('create_league/', views.CreateLeagueView.as_view(), name='create_league'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('members/', include('django.contrib.auth.urls'), name='register'),
    path('members/', include('members.urls'), name='login'),
    path('score_predictions/<int:pk>', views.predictions, name='predictions'),
    path('stats/', views.index, name='stats'),
    path('terms/', views.TermsView.as_view(), name='terms')
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
import django.contrib.auth.urls
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_data, name='home'),
    path('admin/', admin.site.urls),
    path('add_your_bet/', views.AddBetsView.as_view(), name='add_your_bet'),
    path('create_league/', views.CreateLeagueView.as_view(), name='create_league'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



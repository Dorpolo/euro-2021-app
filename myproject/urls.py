from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_data, name='home'),
    path('add_your_bet/', views.AddPostView.as_view(), name='add_your_bet')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
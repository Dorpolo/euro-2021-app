from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from .views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
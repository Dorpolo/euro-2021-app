import django.contrib.auth.urls
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('members/', include('django.contrib.auth.urls'), name='register'),
    path('members/', include('members.urls'), name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
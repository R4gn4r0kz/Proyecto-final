# prototipo/urls.py

from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),       # Página de inicio
    path('', include('shop.urls')),
    path('api/', include('api.urls')),    # APIs propias
    path('shop/', include('shop.urls')),  # Consumo de API externa / vistas shop
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

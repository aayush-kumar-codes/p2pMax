from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import index, user_profile, api_management

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('profile/', user_profile, name='profile'),
    path('api_management/', api_management, name='api_management'),
    path('', index, name="dashboard"),
    path('', include('admin_material.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

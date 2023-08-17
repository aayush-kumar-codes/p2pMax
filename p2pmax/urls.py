from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    index,
    support_tickets,
    system_settings,
    announcements
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', index, name="dashboard"),
    path('support_tickets/', support_tickets, name="support_tickets"),
    path('system_settings/', system_settings, name="system_settings"),
    path('announcements/', announcements, name="announcements"),
    path('', include('admin_material.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

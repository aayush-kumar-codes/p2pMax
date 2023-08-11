from django.contrib import admin
from django.urls import path
from django.urls import path, include

from accounts.views import index, user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('profile/', user_profile, name='profile'),
    path('', index, name="dashboard"),
    path('', include('admin_material.urls')),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Local apps
    path('', include('pages.urls')),
    path('activity/', include('activities.urls')),

    # User management
    path('accounts/', include('allauth.urls')), # I use django-allauth package to signup artists.
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # allow media file store media root after uploaded.

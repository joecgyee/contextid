"""
URL configuration for contextid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Apps 
    path('', include(('apps.core.urls', 'core'), namespace='core')),
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('attributes/', include(('apps.attributes.urls', 'attributes'), namespace='attributes')),
    path('contexts/', include(('apps.contexts.urls', 'contexts'), namespace='contexts')),
    path('profiles/', include(('apps.profiles.urls', 'profiles'), namespace='profiles')),
    path('api/', include(('apps.api.urls', 'api'), namespace='api')),

    path('api-auth/', include('rest_framework.urls')), # Adds "Log In" link to top right of DRF pages
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # FOR PRODUCTION ON RENDER:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

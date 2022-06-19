"""MovieGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from xml.etree.ElementInclude import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
)


urlpatterns = [
    path('',include("movies.urls"), name='home'),
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/ckeditor/', include('ckeditor_uploader.urls')),
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('movies.urls')),
    path('api/v2/',include('account.urls')),
  

     path('api/account/', include('account.api.urls', 'account_api')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('core.urls')
    ),

    path(
        'ai/',
        include('ai.urls')
    ),

    path(
        'users/',
        include('users.urls')
    ),

    path(
        'notes/',
        include('notes.urls')
    ),

    path(
        'history/',
        include('history.urls')
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

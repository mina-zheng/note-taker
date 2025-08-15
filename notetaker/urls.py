from django.urls import path # pyright: ignore[reportMissingModuleSource]

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path('upload/', views.upload_file, name = 'upload_file')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path # type:ignore
from . import views
from django.conf import settings # type:ignore
from django.conf.urls.static import static # type:ignore

urlpatterns = [
    path("", views.index, name="index"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
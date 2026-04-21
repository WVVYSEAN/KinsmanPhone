import mimetypes
import os

from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
]


def serve_media(request, path):
    """Serve uploaded media files from the Railway volume."""
    # Normalise and guard against path traversal
    full_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, path))
    if not full_path.startswith(str(settings.MEDIA_ROOT)):
        raise Http404
    if not os.path.isfile(full_path):
        raise Http404
    content_type, _ = mimetypes.guess_type(full_path)
    return FileResponse(open(full_path, 'rb'), content_type=content_type or 'application/octet-stream')


urlpatterns += [
    re_path(r'^media/(?P<path>.+)$', serve_media),
]

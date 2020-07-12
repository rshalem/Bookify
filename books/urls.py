from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]


# debug True
# configuring MEDIA URL for a MEDIA, eg., 128.0.0.1/images/lappy3.JPG
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
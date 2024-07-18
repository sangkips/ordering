from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib import admin
from decouple import config
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path as url, include

public_apis = [
    url(r'^api/order/', include("apps.orders.urls")),
    url(r'^api/auth/', include("apps.auth_app.urls")),
]

schema_view = get_schema_view(
    openapi.Info(
        title=config("API_TITLE"),
        default_version=config("API_VERSION"),
        description="These are the main APIs for Ordering Application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('developer/docs', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('developer/doc', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
    path('favicon.ico', favicon_view),
    path('admin/', admin.site.urls),
]
urlpatterns += public_apis
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = config('ADMIN_SITE_HEADER')
admin.site.site_title = config('ADMIN_SITE_TITLE')
admin.site.index_title = config('ADMIN_SITE_INDEX_TITLE')


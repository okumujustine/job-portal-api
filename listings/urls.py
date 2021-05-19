
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static, re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("authentication.urls")),

    path('joblisting/', include('job_listing_api.urls', namespace='job_listing_api')),
    path("contactus/", include('contactus.urls')),
    path("", include_docs_urls(title="JobsUg API")),
    path('schema', get_schema_view(
        title="JobsUg API",
        description="API for JobsUg Application",
        version="1.0.0"
    ), name='openapi-schema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# urlpatterns += re_path(r'^(?:.*)/?$',
#                        TemplateView.as_view(template_name='index.html')),


handler404 = "common_utils.views.error_404"
handler500 = "common_utils.views.error_500"

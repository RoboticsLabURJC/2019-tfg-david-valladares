"""jderobot_server URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import handler404, handler500
from jderobot_kids.views import error_handler404, error_handler500
from jderobot_kids.admin import admin_site
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^admin/', include(admin_site.urls)),
    # Add urls to custom views for Admin
    url(r'', include('jderobot_kids.urls')),
    # View to Manage Tag AutoSuggestion
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^uploadArduino/', include('UploadArduino.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = error_handler404
handler500 = error_handler500

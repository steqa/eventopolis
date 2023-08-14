from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('', lambda request: redirect('events/', permanent=True)),
    path('events/', include('events_app.urls')),
    path('user/', include('user_profile.urls')),
    path('tg-notification/', include('telegram_notifications.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

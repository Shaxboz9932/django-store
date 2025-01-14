from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from products.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

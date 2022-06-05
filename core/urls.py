from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('voucher.urls')),
    # path('process/',include('process.urls')),
    path('accounts/',include('accounts.urls')),
    path('acknowledgement/',include('acknowledgement.urls')),
    path('approval/',include('approval.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 

admin.site.index_title = 'Payment Voucher Management'

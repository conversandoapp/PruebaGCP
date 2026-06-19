from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Panel de Administración — Reservas'
admin.site.site_title = 'Reservas Admin'
admin.site.index_title = 'Gestión del Sistema'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.bookings.urls')),
    path('', include('apps.accounts.urls')),
]

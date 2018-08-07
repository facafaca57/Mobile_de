
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('cars.urls')),
    path('load/', include('cars.urls')),
    path('add/', include('cars.urls')),
    path('search/', include('cars.urls')),
    path('admin/', admin.site.urls),
]

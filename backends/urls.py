from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/organization/', include('organization.urls')),
    path('api/system/', include('main.urls'))
]

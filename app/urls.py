from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf/', views.get_csrf, name='api-csrf'),
    path('api/token/connection/', views.get_connection_token, name='api-connection-token'),
    path('api/token/subscription/', views.get_subscription_token, name='api-subscription-token'),
    path('api/login/', views.login_view, name='api-login'),
    path('api/logout/', views.logout_view, name='api-logout'),
    path('api/', include('chat.urls')),
]

urlpatterns += staticfiles_urlpatterns()
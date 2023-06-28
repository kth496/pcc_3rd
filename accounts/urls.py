from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    # 기본 인증 URL
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]

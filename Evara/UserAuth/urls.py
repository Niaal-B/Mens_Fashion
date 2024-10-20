# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name='login'),
    path("register/", views.register, name='register'),
    path('otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('logout/',views.user_logout,name='logout')
]

from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_url, name='create_url'),
    path('s/<str:short_url>', views.redirect_url, name='redirect_url'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('webhook/', views.webhook),
    path('keycloak/', views.keycloak),
]

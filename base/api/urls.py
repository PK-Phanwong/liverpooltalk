from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('contents/', views.getContents),
    path('contents/<str:pk>/', views.getContent),
]
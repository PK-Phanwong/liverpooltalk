from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('content/<str:pk>/', views.content, name="content"), 
    path('creating-content/', views.creatingContent, name="creating-content"),
    path('update-content/<str:pk>/', views.updateContent, name="update-content"),
    path('delete-content/<str:pk>/', views.deleteContent, name="delete-content"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('categories/', views.categoriesPage, name="categories"),
    path('recent-post/', views.recentPost, name="recent-post"),

]
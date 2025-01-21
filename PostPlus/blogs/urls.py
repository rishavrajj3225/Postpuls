
from django.urls import path
from . import views
urlpatterns = [
    path('', views.blog_list,name='allBlogs'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:blog_id>/',views.blog_detail, name='blog_detail'),
    path('<int:blog_id>/update/', views.blog_update, name='blog_update'),
    path('<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    path('register/', views.register, name='register'),
]
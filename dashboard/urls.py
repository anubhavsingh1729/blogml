from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape, name='home'),
    path('index/',views.index,name = 'index'),
    path('post_new/',views.post_new,name = 'post_new'),
    path('post_detail/<int:pk>/',views.post_detail,name='post_detail'),
    path('postlist/',views.getmypost,name = 'postlist'),
]
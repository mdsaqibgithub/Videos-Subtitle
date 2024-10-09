from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_video, name='upload_video'),
    path('videos/', views.video_list, name='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/search/', views.search_subtitles, name='search_subtitles'),
]


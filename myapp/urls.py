from django.urls import path
from . import views


urlpatterns = [
    path('', views.photo_gallery, name='home'),
    path('register/', views.user_registration, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('log_out/', views.log_out, name='logout'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('photo/<int:photo_id>/like/', views.like_post, name='like_photo'),
    path('photo/<int:photo_id>/', views.photo_details, name='photo_detail')
]
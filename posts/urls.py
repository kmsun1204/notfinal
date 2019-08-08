from django.urls import path
from . import views

urlpatterns = [
    path('model/', views.ModelsPageView.as_view(), name='model'),
    path('model/post/', views.CreateModelsView.as_view(), name='model_post'),
    path('model/detail/<int:model_id>/', views.detail, name="model_detail"),
    path('model/detail/<int:model_id>/delete', views.delete, name="delete"),
    path('model/<int:model_id>/edit/', views.edit, name="edit"),

    path('model/filter/cute/', views.filter_cute, name="filter_cute"),
    path('model/filter/cool/', views.filter_cool, name="filter_cool"),
    path('model/filter/bnw/', views.filter_bnw, name="filter_bnw"),
    path('model/filter/plus/', views.filter_plus, name="filter_plus"),

    path('photo/', views.PhotoPageView.as_view(), name="photo"),
    path('photo/post/', views.PhotoCreatePostView.as_view(), name="photo_post"),
    path('photo/detail/<int:photo_id>/', views.photo_detail, name="photo_detail"),
    path('photo/detail/<int:photo_id>/delete', views.photo_delete, name="photo_delete"),
    path('photo/<int:photo_id>/edit/', views.photo_edit, name="photo_edit"),


    path('photo/filter/cute/', views.photo_filter_cute, name="photo_filter_cute"),
    path('photo/filter/cool/', views.photo_filter_cool, name="photo_filter_cool"),
    path('photo/filter/bnw/', views.photo_filter_bnw, name="photo_filter_bnw"),
    path('photo/filter/plus/', views.photo_filter_plus, name="photo_filter_plus"),

]
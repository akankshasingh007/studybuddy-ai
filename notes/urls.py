from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes'),
    path('create/', views.create_note, name='create_note'),
    path('delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('use/<int:pk>/', views.use_note, name='use_note'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.history_list, name='history'),
    path('<int:pk>/', views.session_detail, name='session_detail'),
]
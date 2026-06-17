from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_tool, name='ai_tool'),
    path('export/', views.export_pdf, name='export_pdf'),
]
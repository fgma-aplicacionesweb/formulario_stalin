from django.urls import path
from . import views

urlpatterns = [
    path('datos/', views.consultar_cedula, name='consultar_cedula'),
    path('guardar-datos/', views.guardar_datos, name='guardar_datos'),
]
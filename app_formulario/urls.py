from django.urls import path
from . import views

urlpatterns = [
    path('datos/', views.consultar_cedula, name='consultar_cedula'),
    path('guardar-datos/', views.guardar_datos, name='guardar_datos'),

    path('municipios/<int:estado_id>/', views.get_municipios, name='get_municipios'),
    path('parroquias/<int:municipio_id>/', views.get_parroquias, name='get_parroquias'),
    path('universidades/<int:estado_id>/', views.get_universidades, name='get_universidades'),
    path('direccion-universidad/<int:universidad_id>/', views.get_direccion_universidad, name='get_direccion_universidad'),
    path('personas/', views.lista_personas, name='lista_personas'),
    path('personas/ajax/', views.lista_personas_ajax, name='lista_personas_ajax'),

]

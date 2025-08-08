# models.py
from django.db import models
from django.contrib.auth.models import User

class PersonaRegistro(models.Model):
    cedula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cedula})"
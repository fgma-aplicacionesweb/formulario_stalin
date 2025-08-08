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

    # Guardar la relación con estado / municipio / parroquia
    estado = models.ForeignKey('Estado', on_delete=models.SET_NULL, null=True, blank=True, related_name='personas')
    municipio = models.ForeignKey('Municipio', on_delete=models.SET_NULL, null=True, blank=True, related_name='personas')
    parroquia = models.ForeignKey('Parroquia', on_delete=models.SET_NULL, null=True, blank=True, related_name='personas')
    universidad = models.ForeignKey('Universidad', on_delete=models.SET_NULL, null=True, blank=True, related_name='personas')


    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cedula})"
    
class Direccion(models.Model):
    id_dir = models.AutoField(primary_key=True)
    nom_dir = models.CharField(max_length=350)
    id_par = models.IntegerField()
    id_uni = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'direccion'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Estado(models.Model):
    id_est = models.IntegerField(primary_key=True)
    nom_est = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'estado'


class Municipio(models.Model):
    id_mun = models.AutoField(primary_key=True)
    nom_mun = models.CharField(max_length=50)
    id_est = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_est')

    class Meta:
        managed = False
        db_table = 'municipio'


class Parroquia(models.Model):
    id_par = models.AutoField(primary_key=True)
    nom_par = models.TextField()
    id_mun = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='id_mun')

    class Meta:
        managed = False
        db_table = 'parroquia'


class Universidad(models.Model):
    id_uni = models.AutoField(primary_key=True)
    nomb_uni = models.CharField(max_length=150)
    id_est = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_est')

    class Meta:
        managed = False
        db_table = 'universidad'

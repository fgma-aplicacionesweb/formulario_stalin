# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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

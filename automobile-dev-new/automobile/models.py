from django.db import models
from rest_framework import status


class Cars(models.Model):
    car_id = models.AutoField(primary_key=True, db_column='car_id')
    brand = models.CharField(max_length=100,db_column='brand')
    car_variant = models.CharField(max_length=100, db_column='car_variant')
    car_model = models.CharField(max_length=100, db_column='car_model')
    year_of_production = models.CharField(max_length=100, db_column='year_of_production')
    class Meta:
        managed = True
        db_table = 'cars'


class Users(models.Model):
    email = models.CharField(primary_key=True, max_length=100, db_column='email')
    password = models.CharField(max_length=250,db_column='password',blank=False,null=False)
    name = models.CharField(max_length=100, db_column='name')
    age = models.IntegerField(db_column='age')
    sex = models.CharField(max_length=1, db_column='sex')
    car_id = models.ForeignKey(Cars, models.DO_NOTHING, db_column='car_id',blank=True,null=True)
    fcm_token = models.CharField(max_length=250, db_column='fcm_token')    
    class Meta:
        managed = True
        db_table = 'users'


class BreakingSystem(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250,default="0")
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email')
    L_kampas = models.FloatField(db_column='L_kampas', default=1.0)
    L_cakram = models.FloatField(db_column='L_cakram', default=1.0)
    timestamp = models.DateTimeField(db_column='timestamp')
    class Meta:
        managed = True
        db_table = 'breaking_system'

class TemperatureRise(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250,default="0")
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email')
    temperature = models.FloatField(db_column='temperature')
    timestamp = models.DateTimeField(db_column='timestamp')
    class Meta:
        managed = True
        db_table = 'temperature_rise'


class AirFilter(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250, default="0")    
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email')
    caf = models.FloatField(db_column='caf', default=1.0)
    pressure = models.FloatField(db_column='pressure', default=1.0)
    pressure_drop = models.FloatField(db_column='pressure_drop', default=1.0)        
    timestamp = models.DateTimeField(db_column='timestamp')
    class Meta:
        managed = True
        db_table = 'air_filter'

class FuelSystem(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250,default="0")
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email')
    rpm = models.FloatField(db_column='rpm')
    tps = models.FloatField(db_column='tps')
    fuel_cost = models.FloatField(db_column='fuel_cost')
    timestamp = models.DateTimeField(db_column='timestamp')
    class Meta:
        managed = True
        db_table = 'fuel_system'

class FuelConsumption(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250,default="0")
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    timestamp = models.DateTimeField(db_column='timestamp')
    speed = models.FloatField(db_column='speed', default=1.0)
    t_pos = models.FloatField(db_column='t_pos', default=1.0)
    fcon = models.FloatField(db_column='fcon', default=1.0)
    rpm = models.FloatField(db_column='rpm', default=1.0)
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email')  
        class Meta:
        managed = True
        db_table = 'fuel_consumption'

class CO2(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250,default="0")
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email')
    CO2_per_second = models.FloatField(db_column='CO2_per_second', default=1.0)
    timestamp = models.DateTimeField(db_column='timestamp')
    class Meta:
        managed = True
        db_table = 'CO2'

class OilLifetime(models.Model):
    id_pengambilan = models.CharField(db_column='id_pengambilan', max_length=250,default="0")
    id_model = models.AutoField(primary_key=True, db_column='id_model')
    timestamp = models.DateTimeField(db_column='timestamp')
    olr = models.FloatField(db_column='olr', default=1.0)
    olr_jarak = models.FloatField(db_column='olr_jarak', default=1.0)
    olr_waktu = models.FloatField(db_column='olr_waktu', default=1.0)
    oil_temp = models.FloatField(db_column='oil_temp', default=1.0)
    user_email = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_email') 
    class Meta:
        managed = True
        db_table = 'oil_lifetime' 

class MetadataREST(models.Model):
    """
    Class representation of metadata in Response API.
    Use this class for metadata in Response API
    """
    status = models.IntegerField()
    is_success = models.BooleanField()
    class Meta:
        managed = False


def build_response(status_code, is_success, data, message):
    return {'status_code': status_code, 'is_success': is_success, "message" : message, "data": data}

    #


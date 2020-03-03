from automobile.models import *
from django.core import serializers
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from math import ceil
import math
from datetime import datetime as time
import datetime
from django.db.models import Q
from django.forms.models import model_to_dict as m2d
import jsonpickle as jp
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.db.models import Count
import random
from random import randint as r_int
import numpy as np
import json
import copy
import hashlib as hash



class RootView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'root.html'
    def get(request,self):
        return Response(data=None)

# BUAT APPS 
# BUAT APPS 
# BUAT APPS 
# BUAT APPS  
@api_view(http_method_names=['POST'])
def register(request, format=None):
    try:
        email = request.data.get('email')
        obj = Users.objects.get(email=email)
        obj = m2d(obj)
        err = email + " has already registered"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=[obj]))
    except Users.DoesNotExist:
        email = request.data.get('email')
        password = hash.md5(request.data.get('password').encode()).hexdigest()
        name = request.data.get('name')
        age = request.data.get('age')
        sex = request.data.get('sex')
        fcm_token = request.data.get('fcm_token')
        instance = Users.objects.create(
            email=email,
            password=password,
            name=name,
            age=age,
            sex=sex,
            fcm_token=fcm_token
        )
        instance = m2d(instance)
        m = "register success"
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=[instance]))

@api_view(http_method_names=['POST'])
def auth(request, format=None):
    email = request.data.get('email')
    password = hash.md5(request.data.get('password').encode()).hexdigest()
    try:
        obj = Users.objects.get(email=email,password=password)
        obj = m2d(obj)
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=[obj]))
    except Users.DoesNotExist:
        err = "Something went wrong (email/password)"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))

@api_view(http_method_names=['GET'])
def showAllCar(request, format=None):
    cars_obj = Cars.objects.all()
    data = []
    for i in cars_obj:
        data.append(m2d(i))
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=data))
    
@api_view(http_method_names=['POST'])
def selectCar(request, format=None):
    email_user = request.data.get('user_email')
    try:
        obj_user = Users.objects.get(email=email_user)
        obj_user.car_id = Cars.objects.get(car_id=request.data.get('car_id'))
        instance = m2d(obj_user)
        m = "Success"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=[instance]))
    except Users.DoesNotExist:
        err = "Something went wrong ("+email_user+" not found)"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))


@api_view(http_method_names=['POST'])
def getIntervalCheckBreakingSystem(request, format=None):
    email = request.data.get('user_email')
    request_time = datetime.datetime.strptime(request.data.get('request_time'), '%Y-%m-%d %H:%M:%S')
    data = {}
    obj_break = BreakingSystem.objects.filter(user_email=email)
    if len(obj_break) < 1:
        err = "Something went wrong. " + email + " maybe wrong. Data not found."
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))
        
    try:
        if request_time.day > 14:
            second_week_data_cakram = []
            second_week_data_kampas = []
            for i in obj_break:
                current_req = i.timestamp
                if current_req.day > 15 and request_time.month == current_req.month and request_time.year == current_req.year:
                    second_week_data_cakram.append(float(i.L_kampas))
                    second_week_data_kampas.append(float(i.L_cakram))
            
                data['avg_first_week_kampas'] = 0 if math.isnan(round(np.average(second_week_data_kampas),3)) else round(np.average(second_week_data_kampas),3)
                data['avg_first_week_cakram'] = 0 if math.isnan(round(np.average(second_week_data_cakram),3)) else round(np.average(second_week_data_cakram),3)
        else:
            first_week_data_cakram = []
            first_week_data_kampas = []
            for i in obj_break:
                current_req = i.timestamp
                if current_req.day <= 15 and request_time.month == current_req.month and request_time.year == current_req.year:
                    first_week_data_cakram.append(float(i.L_kampas))
                    first_week_data_kampas.append(float(i.L_cakram))
            
                data['avg_first_week_kampas'] = 0 if math.isnan(round(np.average(first_week_data_kampas),3)) else round(np.average(first_week_data_kampas),3)
                data['avg_first_week_cakram'] = 0 if math.isnan(round(np.average(first_week_data_cakram),3)) else round(np.average(first_week_data_cakram),3)
        print(request_time)
        print(data)
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=[data]))
    except ValueError:
        err = "NaN value"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))

@api_view(http_method_names=['POST'])
def getBreakingSystemByEmail(request, format=None):
    email = request.data.get('user_email')
    obj_break = BreakingSystem.objects.extra(select={'day':'date(timestamp)'}).values('day').annotate(avg_reduction_expectancy_kampas=Avg('L_kampas'), avg_reduction_expectancy_cakram=Avg('L_cakram')).order_by('day').filter(user_email=email)
    data = []
    if len(obj_break) > 0:
        CONST_kampas = 30000
        CONST_cakram = 60000
        for i in obj_break:
            CONST_kampas -= i["avg_reduction_expectancy_kampas"]
            i['remaining_life_kampas'] = CONST_kampas
            CONST_cakram -= i["avg_reduction_expectancy_cakram"]
            i['remaining_life_cakram'] = CONST_cakram

            data.append(i)

    else:        
        err = "No breaking system data"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))

    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=data))


@api_view(http_method_names=['POST'])
def getTemperatureRiseByEmail(request, format=None):
    email = request.data.get('user_email')
    obj_temperature = TemperatureRise.objects.filter(user_email=email)
    data = {
        'occurrences_within_range' : [],
        'occurrences_below_range' : [],
        'occurrences_above_range' : []
    }
    if len(obj_temperature) > 0:
        list_of_attempt = []

        for i in obj_temperature:
            if i.id_pengambilan not in list_of_attempt:
                list_of_attempt.append(int(i.id_pengambilan))
        
        max_attempt = np.max(list_of_attempt)
        list_at_latest_attempt = []

        data['id_occurrence'] = max_attempt

        for i in obj_temperature:
            if int(i.id_pengambilan) == max_attempt:
                list_at_latest_attempt.append(float(i.temperature))
        data['attempts'] = len(list_at_latest_attempt)
        counter_within_range = 0
        counter_below_range = 0
        counter_above_range = 0
        for i in list_at_latest_attempt:
            if i >= 100 and i <= 250:
                counter_within_range += 1
                data['occurrences_within_range'].append(i)
            elif i < 100:
                counter_below_range += 1
                data['occurrences_below_range'].append(i)
            elif i > 250:
                counter_above_range += 1
                data['occurrences_above_range'].append(i)
            data['counter_occurrences_below_range'] = counter_below_range
            data['counter_occurrences_within_range'] = counter_within_range
            data['counter_occurrences_above_range'] = counter_above_range
    else:        
        err = "No temperature rise data"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))
        
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=[data]))

    


@api_view(http_method_names=['POST'])
def getAirFilterByEmail(request, format=None):
    email = request.data.get('user_email')
    obj_airfilter = AirFilter.objects.filter(user_email=email)
    data = None
    
    if len(obj_airfilter) > 0:
        counted = []
        for i in obj_airfilter:
            counted.append(int(i.id_pengambilan))
        max = np.max(counted)
        output = []
        timestamp = None
        for i in obj_airfilter:
            if int(i.id_pengambilan) == max:
                output.append(float(i.caf))
                timestamp = i.timestamp
        avg_caf = np.average(output)
        
        data = {
            "timestamp" : timestamp,
            "avg_caf" : avg_caf            
        }
    else:        
        err = "No air filter data"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))
        
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=[data]))

@api_view(http_method_names=['POST'])
def getFuelSystemByEmail(request, format=None):
    email = request.data.get('user_email')
    # obj_fuel = FuelSystem.objects.filter(user_email=email)
    
    obj_fuel = FuelSystem.objects.extra(select={'trip':'id_pengambilan'}).values('trip').annotate(avg_rpm=Avg('rpm'),avg_tps=Avg('tps'),trip_cost=Sum('fuel_cost'),fuel_cost=Avg('fuel_cost')).order_by('trip').filter(user_email=email)
    data = []
    if len(obj_fuel) > 0:
        for i in obj_fuel:
            data.append(i)
    else:        
        err = "No air filter data"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))
        
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=data))

@api_view(http_method_names=['POST'])
def getEstimatedLifetimeAirFilter(request, format=None):
    email = request.data.get('user_email')
    obj_air = AirFilter.objects.filter(user_email=email)
    trip = []
    data = None
    const_distance = 48000
    myu_drive = 72.26666667
    if len(obj_air) > 0:
        for i in obj_air:
            if int(i.id_pengambilan) not in trip:
                trip.append(int(i.id_pengambilan))
        max = np.max(trip)

        avg = []
        pressure = []
        total_data = 0
        trip_max = []
        timestamp = None
        for i in obj_air:
            if int(i.id_pengambilan) == max:
                trip_max.append(i)
                timestamp = i.timestamp
        total_data = len(trip_max)
        for i in trip_max:
            avg.append(float(i.caf))
            pressure.append(float(i.pressure_drop))
        
        avg_caf = np.average(avg)
        pressure_drop = np.sum(pressure)
        estimated_time_left = estimatedAirFilter(avg_caf, pressure_drop, total_data)
        estimated_distance_left = estimatedDinstanceLeft(const_distance, myu_drive)
        data = {
            "timestamp" : timestamp,
            "avg_caf" : avg_caf,
            "estimated_time_left" : estimated_time_left,
            "estimated_distance_left" : estimated_distance_left
        }


    else:
        err = "No air filter data"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))
        
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=[data]))

@api_view(http_method_names=['POST'])
def getAirFilterByEmailGroupByMonth(request, format=None):
    email = request.data.get('user_email')
    const_distance = 48000
    myu_drive = 72.26666667
    obj_air = AirFilter.objects.annotate(month=TruncMonth('timestamp')).values('month').annotate(avg_air_filter=Avg('caf'),sum_pressure_drop=Sum('pressure_drop'),length_data=Count('caf')).order_by('month').filter(user_email=email)
    data = []
    length = len(obj_air)
    if len(obj_air) > 0:
        for i in obj_air:
            i['estimated_time_left'] = estimatedAirFilter(i['avg_air_filter'], i['sum_pressure_drop'], i['length_data'])
            i['estimated_distance_left'] = estimatedDinstanceLeft(const_distance, myu_drive)
            data.append(i)
    else:        
        err = "No air filter data"
        return Response(build_response(status_code=status.HTTP_404_NOT_FOUND,is_success=False,message=err,data=None))    
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message="",data=data))


def estimatedAirFilter(avg_caf, pressure_drop, total_data):
    lower = 0.98 * ( ( (100-avg_caf) * (total_data - 1) ) + (pressure_drop/(total_data-1)) )/3017
    return avg_caf/lower

def estimatedDinstanceLeft(const, myu_drive):
    # const = 48000
    # myu_drive = 72.26666667
    Xt = const - (1095 * (myu_drive-(0.966*myu_drive)))
    return Xt

# BUAT RASPI
# BUAT RASPI
# BUAT RASPI
# BUAT RASPI
# BUAT RASPI
@api_view(http_method_names=['POST'])
def insertBreakingSystem(request, format=None):
    try:
        for row in request.data:
            print(row)
            obj_user = Users.objects.get(email=row['user_email'])
            instance = BreakingSystem.objects.create(
                user_email=obj_user,
                L_kampas=row['L_kampas'],
                L_cakram=row['L_cakram'],
                id_pengambilan=row['id_pengambilan'],
                timestamp=row['timestamp']
            )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))

@api_view(http_method_names=['POST'])
def insertBreakingSystemSpecialCase(request, format=None):
    try:
        for row in request.data:
            print(row)
            obj_user = Users.objects.get(email=row['user_email'])
            timestamp = row['timestamp']
            year = timestamp[6:10]
            month = timestamp[3:5]
            day = r_int(10,59)
            exc_time = timestamp[11:len(timestamp)]
            new_timestamp = year + "-" + month + "-" + day + " " + exc_time + "+00"
            
            instance = BreakingSystem.objects.create(
                user_email=obj_user,
                L_kampas=row['L_kampas'],
                L_cakram=row['L_cakram'],
                id_pengambilan=row['id_pengambilan'],
                timestamp=new_timestamp
            )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))


@api_view(http_method_names=['POST'])
def insertTemperatureRise(request, format=None):
    try:
        for row in request.data:
            obj_user = Users.objects.get(email=row['user_email'])
            instance = TemperatureRise.objects.create(
                user_email=obj_user,
                temperature=row['temperature'],
                id_pengambilan=row['id_pengambilan'],
                timestamp=row['timestamp']
            )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))


@api_view(http_method_names=['POST'])
def insertTemperatureRiseSpecialCase(request, format=None):
    try:
        for row in request.data:
            obj_user = Users.objects.get(email=row['user_email'])
            timestamp = row['timestamp']
            year = timestamp[6:10]
            month = timestamp[3:5]
            day = r_int(10,59)
            exc_time = timestamp[11:len(timestamp)]
            new_timestamp = year + "-" + month + "-" + day + " " + exc_time + "+07"

            
            instance = TemperatureRise.objects.create(
                user_email=obj_user,
                temperature=row['temperature'],
                id_pengambilan=row['id_pengambilan'],
                new_timestamp=row['timestamp']
            )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))


@api_view(http_method_names=['POST'])
def insertAirFilter(request, format=None):
    try:
        for row in request.data:
            obj_user = Users.objects.get(email=row['user_email'])
            if caf >= 10 and caf <= 99:
                pressure = float(row['pressure'])
                instance = AirFilter.objects.create(
                    user_email=obj_user,
                    caf=caf,
                    id_pengambilan=row['id_pengambilan'],
                    pressure=row['pressure'],
                    timestamp=row['timestamp'] 
                )
                instance.pressure_drop = 58537.89 - instance.pressure
                instance.save()

        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))

@api_view(http_method_names=['POST'])
def insertFuelSystem(request, format=None):
    try:
        for row in request.data:
            user = Users.objects.get(email=row['user_email'])
            rpm = row['rpm']
            tps = row['tps']
            fuel_cost = row['fuel_cost']
            if rpm != "None" and tps != "None" and fuel_cost != "None":
                instance = FuelSystem.objects.create(
                    user_email=user,
                    rpm=rpm,
                    id_pengambilan=row['id_pengambilan'],
                    tps=tps,
                    fuel_cost=fuel_cost,
                    timestamp=row['timestamp'] 
                )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))

@api_view(http_method_names=['POST'])
def insertEmmisionSystem(request, format=None):
    try:
        for row in request.data:
            print(row)
            obj_user = Users.objects.get(email=row['user_email'])
            CO2_per_second = row['CO2_per_second']
            if CO2_per_second != "None":
                instance = CO2.objects.create(
                    user_email=obj_user,
                    CO2_per_second=CO2_per_second,
                    id_pengambilan=row['id_pengambilan'],
                    timestamp=row['timestamp']
            )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))

@api_view(http_method_names=['POST'])
def insertOilLifetime(request, format=None):
    try:
        for row in request.data:
            user = Users.objects.get(email=row['user_email'])
            rps = row['rps']
            olr = row['olr']
            akumulatif_rps = row['akumulatif_rps']
            olr_jarak = row['olr_jarak']
            olr_waktu = row['olr_waktu']
            oil_temp = row['oil_temp']
            if olr != "None" and olr_jarak != "None" and olr_waktu != "None" and oil_temp != "None":
                instance = FuelConsumption.objects.create(
                    user_email=user,
                    id_pengambilan=row['id_pengambilan'],
                    rps=rps,
                    olr=olr,
                    akumulatif_rps=akumulatif_rps,
                    olr_jarak=olr_jarak,
                    olr_waktu=olr_waktu,
                    oil_temp=oil_temp,
                    timestamp=row['timestamp'] 
                )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))

@api_view(http_method_names=['POST'])
def insertFuelConsumption(request, format=None):
    try:
        for row in request.data:
            user = Users.objects.get(email=row['user_email'])
            speed = row['speed']
            t_pos = row['t_pos']
            fcon = row['fcon']
            rpm = row['rpm']
            if speed != "None" and t_pos != "None" and fcon != "None" and rpm != "None":
                instance = FuelConsumption.objects.create(
                    user_email=user,
                    id_pengambilan=row['id_pengambilan'],
                    speed=speed,
                    t_pos=t_pos,
                    fcon=fcon,
                    rpm=rpm,
                    timestamp=row['timestamp'] 
                )
        m = "Success adding data"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=None))            
    except Users.DoesNotExist:
        err = "NOT FOUND"
        return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=err,data=None))

# MISC
# MISC
# MISC
@api_view(http_method_names=['POST'])
def insertCar(request, format=None):
    data = []
    for row in request.data:
        instance = Cars.objects.create(
            brand=row['brand'],
            car_variant=row['car_variant'],
            car_model=row['car_model'],
            year_of_production=row['year_of_production'] 
        )
        data.append(m2d(instance))
    m = "Success"
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=data))            


@api_view(http_method_names=['POST'])
def seedFuelData(request, format=None):
    data = []
    for row in request.data:
        user = Users.objects.get(email=row['user_email'])
        rpm = row['rpm']
        tps = row['tps']
        fuel_cost = row['fuel_cost']
        if rpm != "None" and tps != "None" and fuel_cost != "None":
            instance = FuelSystem.objects.create(
                user_email=user,
                rpm=rpm,
                id_pengambilan=row['id_pengambilan'],
                tps=tps,
                fuel_cost=fuel_cost,
                timestamp=row['timestamp'] 
            )
            data.append(m2d(instance))
    m = "Success"
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=data))            

@api_view(http_method_names=['POST'])
def seedBreakingData(request, format=None):
    data = []
    for row in request.data:
        user = Users.objects.get(email=row['user_email'])
        instance = BreakingSystem.objects.create(
            user_email=user,
            id_pengambilan=row['id_pengambilan'],
            L_kampas=row['L_kampas'],
            L_cakram=row['L_cakram'],
            timestamp=row['timestamp'] 
        )
        data.append(m2d(instance))
    m = "Success"
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=data))            

@api_view(http_method_names=['POST'])
def seedTemperatureData(request, format=None):
    data = []
    for row in request.data:
        user = Users.objects.get(email=row['user_email'])
        instance = TemperatureRise.objects.create(
            user_email=user,
            id_pengambilan=row['id_pengambilan'],
            temperature=row['temperature'],
            timestamp=row['timestamp'] 
        )
        data.append(m2d(instance))
    m = "Success"
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=data))            

@api_view(http_method_names=['POST'])
def seedAirFilter(request, format=None):
    data = []
    for row in request.data:
        user = Users.objects.get(email=row['user_email'])
        caf = float(row['caf']) * 100
        if caf >= 10 and caf <= 90:
            instance = AirFilter.objects.create(
                user_email=user,
                caf=caf,
                id_pengambilan=row['id_pengambilan'],
                timestamp=row['timestamp'] 
            )
            data.append(m2d(instance))
    m = "Success"
    return Response(build_response(status_code=status.HTTP_200_OK,is_success=True,message=m,data=data))            


from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import viewsets
from rest_framework import response
from django.core.cache import cache
from datetime import datetime
import json
import requests

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
BASE_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/"

# Create your views here.
@api_view(['GET'])
def ping(request):
	return JsonResponse({'data':'Pong'})

def wind(data):
    wind_info= data
    if wind_info.find('G') != -1:
        wind_direction= wind_info[0:3]
        wind_velocity= wind_info[3:5]
        wind_gust= wind_info[6:8]
        print(wind_gust)
    else:
        wind_direction= wind_info[0:3]
        wind_velocity= wind_info[3:5]
        wind_gust= 0
        print(wind_gust)
    if int(wind_gust) > 0:
        wind_details_str= str(wind_direction) + " degree at the speed of  "+str(wind_velocity)+ " knots with "+ str(wind_gust)+" knot gusts"
    else:
        wind_details_str= str(wind_direction) + " degree at the speed of "+str(wind_velocity)+ " knots"
    return wind_details_str

def temperature(data):
    temperature_info= data.split('/')
    temperature= temperature_info[0]
    if 'M' in temperature:
        temp_fer = (int(str(temperature.replace('M','')))*9/5)+32
        temperature= str(temperature.replace('M','-')) + " degree Celcius"
    else:
        temp_fer = (int(str(temperature))*9/5)+32
        
        temperature= str(temperature) + 'degree Celcius'
    
    temperature_str= temperature + "(" +str(temp_fer)+ " f)"
    return temperature_str

@api_view(['GET'])
def scodeDetails(request):
    wind_details_str= ""
    temperature_str= ""

    if "nocache" in request.GET and "scode" in request.GET:

        nocache= request.GET["nocache"]
        refresh_cache= False
        if nocache == "0" and request.GET["scode"] in cache:
            
            cache_response= cache.get(request.GET["scode"])
            cache_response['nocache']= nocache
            cache_response['fetch_from']= "CACHE"

            return JsonResponse({'data': cache_response})
        elif nocache == "1":
            r= requests.get(BASE_URL+ request.GET["scode"]+'.TXT')
            data_group= r.text.split('\n')
            last_observation= data_group[0]
            other_info= data_group[1].split(' ')

        for data in other_info:
            if data.endswith('KT'):
                wind_details_str= wind(data)

            if data.find('/') != -1:

                    temperature_str= temperature(data)

        
        last_observation_list =last_observation.split(' ')
        last_observation_str= last_observation_list[0]+ " at " + last_observation_list[1]+ " GMT "
        
        responsejson= {}
        responsejson['station']= request.GET["scode"]
        responsejson['last_observation']= last_observation_str
        responsejson['temperature']= temperature_str
        responsejson['wind']= wind_details_str
        responsejson['Current_record_time']= datetime.now()

        cache.set(request.GET["scode"], responsejson, timeout= CACHE_TTL)

        responsejson['nocache']= nocache

        return JsonResponse({'data': responsejson})
    else:
            return JsonResponse({'msg':"Please set nocache value to 1 for refreshed scode"})

    return JsonResponse({'msg':"Please set nocache value to 0 or 1."})
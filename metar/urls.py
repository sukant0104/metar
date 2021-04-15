from django.urls import path,include
from .views import *
from rest_framework import routers
from django.db import router



router= routers.DefaultRouter()

urlpatterns = [
    path('ping/', ping, name='ping'),
    path('info/', scodeDetails, name="scodeDetails"),

    path('', include(router.urls)),
]



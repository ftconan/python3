"""
@author: magician
@file:   urls.py
@date:   2021/3/24
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]

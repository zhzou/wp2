from django.urls import path

from . import views

urlpatterns = [
path('', views.getscore, name='getscore'),
]
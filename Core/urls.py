from django.urls import path
from .views import allresult



urlpatterns = [
    path('allresult/', allresult, name='allresult'),
]

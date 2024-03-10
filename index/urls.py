from django.urls import path
from .views import home

app_name = 'index'

urlpatterns = [
    path('', home, name="home")
]

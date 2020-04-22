from django.urls import path
from . import views

# URL pattern is an empty string
# view function that will be called if the URL pattern is detected : views.index()
urlpatterns = [
    path('', views.index, name='index'),
]
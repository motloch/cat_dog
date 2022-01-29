from django.urls import path

from . import views

app_name = 'cat_dog_site'
urlpatterns = [
    path('', views.index, name='index'),
]

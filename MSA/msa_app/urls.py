from django.urls import path
from . import views

app_name = 'msa_app'

urlpatterns = [
    path('', views.HomePage, name='index'),
    path('createuser/', views.CreateUser, name='create-user'),
    path('createmed/', views.CreateMedicine, name='create-medicine'),
]
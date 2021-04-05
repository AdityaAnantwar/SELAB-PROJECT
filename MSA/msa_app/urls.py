from django.urls import path
from . import views

app_name = 'msa_app'

urlpatterns = [
    path('', views.HomePage, name='index'),
    path('login/', views.EmployeeLogin, name='login'),
    path('createuser/', views.CreateUser, name='create-user'),
    path('createmed/', views.CreateMedicine, name='create-medicine'),
    path('createven/', views.CreateVendor, name='create-vendor'),
    path('addstock/', views.AddStock, name='add-stock'),
    path('allmedicines/', views.TableMedicines, name='all-medicines'),
    path('allvendors/', views.TableVendors, name='all-vendors'),
    path('allemployees/', views.TableEmployees, name='all-employees'),
    path('expiredmedicines/', views.TableExpired, name='expired-medicines'),
    path('purchasemedicines/', views.TablePurchase, name='purchase-medicines'),
    path('revenueprofit/', views.RevenueProfitView, name='revenue-profit')
]
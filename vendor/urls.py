"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.urls import path
from . import views


app_name = 'vendor'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('products/', views.product_all, name='products'),
    path('pallys/', views.pally_all, name = 'pallys'),
    path('orders/', views.orders_all, name='orders'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit/products/<product_id>', views.edit_product, name='edit_product'),
    path('delete/products/<product_id>', views.delete_product, name='delete_product'),
    path('edit-detials/', views.edit_details, name='edit_details')
]

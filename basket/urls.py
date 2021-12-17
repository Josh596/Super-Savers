from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('create_pally/', views.create_pally, name='basket_create_pally'),
    path('add_pally/', views.pallybasket_add, name='basket_add_pally'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('delete/pally', views.pallybasket_delete, name='pallybasket_delete'),
    path('update/pally', views.pallybasket_update, name='pallybasket_update'),
    path('update/', views.basket_update, name='basket_update'),
]
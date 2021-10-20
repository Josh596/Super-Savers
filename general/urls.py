from django.urls import path

from . import views

app_name = 'general'

urlpatterns = [
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('help-center/', views.help_center, name='help_center'),
    path('promo-discount/', views.promo_discount, name='promo_discount'),
    path('terms-and-conditions/', views.terms_conditions, name='terms_and_conditions')
]
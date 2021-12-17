from django.shortcuts import render
from django.contrib import messages

from general.forms import ContactRequestForm




def about_us(request):
    return render(request, 'general/about-us.html')

def contact_us(request):
    form = ContactRequestForm(request.POST or None)
    if request.method == 'POST':
        form.save()

    #Pass the contact us form here
    return render(request, 'general/contact-us.html', {'contact_form':form})

def help_center(request):
    return render(request, 'general/help-center.html')

def promo_discount(request):
    return render(request, 'general/promo-discount.html')

def terms_conditions(request):
    return render(request, 'general/terms-conditions.html')
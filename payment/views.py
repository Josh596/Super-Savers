import json
import os
import hashlib
from datetime import date, datetime, timedelta
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.conf import settings
from stripe.api_resources import payment_intent
from basket.views import get_subtotal_price, get_total_price
from pypaystack import Transaction
from basket.basket import Basket, PallyBasket
from orders.views import payment_confirmation

from .unique_order_key_gen import unique_order_key_generator

def order_placed(request):
    basket = Basket(request)
    pallybasket = PallyBasket(request)
    for item in pallybasket:
        pally = item['pally']
        print(pally)
        if not pally.is_active:
            pally.is_active = True
        if not pally.author:
            pally.author = request.user
        pally.members.add(request.user)
        pally.available_slots -= item['qty']
        pally.expiry_date = datetime.utcnow() + timedelta(days = 2)
        pally.save()
    basket.clear()
    pallybasket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required
def BasketView(request):

    basket = Basket(request)
    pallybasket = PallyBasket(request)
    total = str(round(basket.get_total_price() + pallybasket.get_total_price(), 2))

    total = total.replace('.', '')
    total = int(total)

    order_key = unique_order_key_generator()
    pk_public = settings.PAYSTACK_PUBLIC_KEY
    total = get_total_price(request)
    subtotal = get_subtotal_price(request)
    return render(request, 'payment/payment_form.html', {'PAYSTACK_PUBLIC_KEY':pk_public, 
                                                    'basket':basket, 'order_key':order_key,
                                                     'total_cost':total, 'subtotal_cost':subtotal})


def verify(request, ref):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(ref)
    data = JsonResponse(response, safe=False)
    payment_confirmation(ref)
    return data

@csrf_exempt
def paystack_webhook(request):
    secret = settings.PAYSTACK_SECRET_KEY
    hash = hashlib.sha512(secret).update(json.dumps(request.body)).hexdigest()

    if (hash == request.headers['x-paystack-signature']): 
        #Retrieve the request's body
        event = request.body
        #Do something with event  
    

    event = None

    # Handle the event
    
    if event['event'] == 'charge.success':
        print('Payment Succeeded')
        payment_confirmation(event['data']['reference'])

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

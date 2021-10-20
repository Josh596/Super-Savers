import json
import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
from stripe.api_resources import payment_intent
from pypaystack import Transaction
from basket.basket import Basket, PallyBasket
from orders.views import payment_confirmation

from .unique_order_key_gen import unique_order_key_generator

def order_placed(request):
    basket = Basket(request)
    pallybasket = PallyBasket(request)
    for item in pallybasket:
        pally = item['pally']
        if not pally.is_active:
            pally.is_active = True
        pally.members.add(request.user)
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
    return render(request, 'payment/payment_form.html', {'PAYSTACK_PUBLIC_KEY':pk_public, 'basket':basket, 'order_key':order_key})


def verify(request, ref):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    payment_confirmation(ref)
    return data

@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Try to validate and create a local instance of the event
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e



    # Handle the event
    
    if event['type'] == 'payment_intent.succeeded':
        print('Payment Succeeded')
        payment_confirmation(event['data']['object']['client_secret'])

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

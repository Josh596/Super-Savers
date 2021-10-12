import json
import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
from stripe.api_resources import payment_intent

from basket.basket import Basket, PallyBasket
from orders.views import payment_confirmation


def order_placed(request):
    basket = Basket(request)
    pallybasket = PallyBasket(request)
    for item in pallybasket:
        pally = item['pally']
        if not pally.is_active:
            pally.is_active = True
        pally.members.add(request.user)
        pally.save()
    print(pallybasket.__len__(), 'As 200000')
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

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret, 
                                                            'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')})


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

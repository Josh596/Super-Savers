from django.http.response import JsonResponse
from django.shortcuts import render

from basket.basket import Basket, PallyBasket
from store.models import Pally

from .models import Order, OrderItem, PallyOrderItem


def add(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()
        pally_basket_total = pally_basket.get_total_price()
        baskettotal = baskettotal + pally_basket_total

        #Check if product is still in stock
        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                address2='add2', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

            for item in pally_basket:
                PallyOrderItem.objects.create(order_id=order_id, product=item['pally'], price=item['price'], quantity=item['qty'])
        response = JsonResponse({'success': 'Return something'})
        return response



def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


    
    #Activate any pally when payment is confirmed here
    #If pally is already active, add user to pally


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
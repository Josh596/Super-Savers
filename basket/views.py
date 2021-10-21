from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from store.models import Pally, Product, Price, Unit

from .basket import Basket, PallyBasket


def get_total_qty(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)

    basketqty = basket.__len__() + pally_basket.__len__()
    
    return basketqty

def get_total_price(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)

    basketprice = basket.get_total_price() + pally_basket.get_total_price()
    
    return basketprice

def get_subtotal_price(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)

    basketprice = basket.get_subtotal_price() + pally_basket.get_subtotal_price()
    
    return basketprice

def basket_summary(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)
    price = get_total_price(request)
    return render(request, 'basket/cart.html', {'basket': basket, 'pally_basket':pally_basket, 'total_cost':price})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = get_total_qty(request)
        response = JsonResponse({'qty': basketqty})
        return response

def pallybasket_add(request):
    basket = PallyBasket(request)
    if request.POST.get('action') == 'post':
        pally_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        pally = get_object_or_404(Pally, id=pally_id)
        if pally.available_slots > 0:
            basket.add(pally=pally, qty=product_qty)
            basketqty = get_total_qty(request)
            response = JsonResponse({'qty': basketqty})
            return response
        else:
            return JsonResponse({'message': 'Pally has maxiumum number of members. Sorry'}, status=400)

def create_pally(request):
    basket = PallyBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        no_of_persons = int(request.POST.get('no_of_person'))
        product = get_object_or_404(Product, id=product_id)
        unit = product.price.unit
        #Default unit for Pally is slot

        price_object = Price.objects.create(
            unit = unit,
            quantity = round(product.price.quantity/no_of_persons, 2),
            price = product.get_discount_price()/no_of_persons
        )
        

        pally = Pally.objects.create(
            author = None,
            product = product,
            price_per_slot = price_object,
            max_num_slot = no_of_persons,
            is_active = False
        )
        

        basket.add(pally=pally, qty=product_qty)

        basketqty = get_total_qty(request)
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = get_total_qty(request)
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def pallybasket_delete(request):
    basket = PallyBasket(request)
    if request.POST.get('action') == 'post':
        pally_id = int(request.POST.get('productid'))
        basket.delete(pally=pally_id)

        basketqty = get_total_qty(request)
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal})
        return response

def pallybasket_update(request):
    basket = PallyBasket(request)
    if request.POST.get('action') == 'post':
        pally_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(pally=pally_id, qty=product_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal})
        return response
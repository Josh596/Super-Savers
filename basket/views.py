from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Pally, Product

from .basket import Basket, PallyBasket


def basket_summary(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)
    return render(request, 'basket/cart.html', {'basket': basket, 'pally_basket':pally_basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def create_pally(request):
    basket = PallyBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        no_of_persons = int(request.POST.get('no_of_person'))
        product = get_object_or_404(Product, id=product_id)
        if request.user:
            pally = Pally.objects.create(
                author = request.user,
                product = product,
                price_per_slot = product.price.price/no_of_persons,
                max_num_slot = no_of_persons,
                is_active = False
            )
            pally.save()
        basket.add(pally=pally, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
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
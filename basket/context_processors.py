from .basket import Basket, PallyBasket


def basket(request):
    basket = Basket(request)
    pally_basket = PallyBasket(request)
    length = basket.__len__() + pally_basket.__len__()

    return {'basket_total': length}


    
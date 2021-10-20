from django.core.exceptions import FieldError
from django.db.models import Sum
from orders.models import OrderItem



def ordercount(request):
    pending_orders = 0
    amount_earned = 0
    try:
        vendor = request.user.vendor
        pending_orders = OrderItem.objects.filter(product__vendor = vendor, status = 1)
        completed_orders = OrderItem.objects.filter(product__vendor = vendor, status = 2)
        
        pending_orders = pending_orders.count()

        if completed_orders.exists():
            amount_earned = completed_orders.aggregate(Sum('price'))
    except AttributeError:
        pass



    return {'pending_orders':pending_orders, 'vendor_amount_earned': amount_earned}
            

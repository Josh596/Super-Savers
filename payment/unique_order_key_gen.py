import random
import string

from orders.models import Order


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_key_generator():
    order_new_id= random_string_generator()


    qs_exists= Order.objects.filter(order_key= order_new_id).exists()
    if qs_exists:
        return unique_order_key_generator()
    return order_new_id
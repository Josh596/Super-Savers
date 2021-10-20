from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db.utils import IntegrityError
from account.tokens import account_activation_token
from orders.models import OrderItem
from store.models import Price, Product, Pally
from vendor.forms import AddProductForm, PriceCreationForm, VendorRegistrationForm
from vendor.models import Vendor

# Create your views here.

###############################
# CHECK THAT USER IS A VENDOR #
###############################
def is_vendor_test(user):
    is_vendor = False
    try:
        user.vendor
        is_vendor = True
    except ObjectDoesNotExist:
        is_vendor = False
    
    return is_vendor

def not_vendor_test(user):
    is_vendor = False
    try:
        user.vendor
        is_vendor = True
    except ObjectDoesNotExist:
        is_vendor = False
    
    return not is_vendor


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@login_required
@user_passes_test(not_vendor_test, login_url='/vendor/')
def register(request):
    register_form = VendorRegistrationForm(initial = {'business_email': request.user.email})
    
    if request.method == 'POST':
        register_form = VendorRegistrationForm(request.POST ,request.FILES)
        if register_form.is_valid():
            form = register_form.save(commit=False)
            form.user = request.user
            form.save()

        
        return redirect('vendor:dashboard')

    return render(request, 'vendor/register.html', {'form':register_form})

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def index(request):
    return redirect('vendor:dashboard')

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def dashboard(request):
    return render(request, 'vendor/dashboard.html')

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def product_all(request):
    vendor = request.user.vendor
    products = vendor.store_product_related.all()
    
    return render(request, 'vendor/product-all.html', {'products':products})

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def pally_all(request):
    vendor = request.user.vendor
    pallys = vendor.store_pally_related.all()
    return render(request, 'vendor/pally-all.html', {'pallys':pallys})

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def orders_all(request):
    vendor = request.user.vendor
    product = vendor.store_product_related.all()
    orders = OrderItem.objects.filter(product__in = product, order__billing_status=True).order_by('-status')
    status =  {
                1: 'Not Yet Shipped',
                2: 'Shipped',
                3: 'Cancelled',
                4: 'Refunded',
            }   
    #In templates, render fulfilled orders and non-fulfilled orders
    return render(request, 'vendor/orders-all.html', {'orders': orders, 'status':status})
    

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def edit_product(request, product_id):
    vendor = request.user.vendor
    products = vendor.store_product_related.all()
    product = get_object_or_404(products, id = product_id)
    form = AddProductForm(request.POST or None,request.FILES or None,instance = product)
    price_form = PriceCreationForm(request.POST or None, instance=product.price)
    if request.method == 'POST':
        if form.is_valid():
            price_form.save()
            new_product = form.save(commit=False)
            new_product.vendor = vendor
            new_product.save()
            form.save_m2m()
        return redirect('vendor:products')

    return render(request, 'vendor/product-edit.html', {'product':product, 'form':form})

# @login_required
# @user_passes_test(is_vendor_test, login_url='/vendor/register/')
# def edit_pally(request, pally_id):
#     vendor = request.user.vendor
#     pallys = vendor.store_pally_related.all()
#     pally = get_object_or_404(pallys, id = pally_id)
#     pally_form = AddPallyForm(request.POST or None,request.FILES or None, instance = pally)
#     if request.method == 'POST':
#         if pally_form.is_valid():
#             new_pally = pally_form.save(commit=False)
#             new_pally.vendor = vendor
#             new_pally.save()
#             pally_form.save_m2m()
        
#         return redirect('vendor:pallys')

#     return render(request, 'vendor/pally-edit.html', {'pally':pally, 'form':pally_form})


@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def edit_details(request):
    pass

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def add_product(request):
    vendor = request.user.vendor
    product_form = AddProductForm(request.POST or None, request.FILES or None)
    price_form = PriceCreationForm(request.POST or None)
    if request.method == 'POST':
        if product_form.is_valid() and price_form.is_valid():
            price = price_form.save()
            new_product = product_form.save(commit=False)
            new_product.price = price
            new_product.vendor = vendor
            new_product.save()
            product_form.save_m2m()

        return redirect('vendor:products')

    return render(request, 'vendor/product-edit.html', {'form':product_form, 'price_form':price_form})


# @login_required
# @user_passes_test(is_vendor_test, login_url='/vendor/register/')
# def add_pally(request):
#     vendor = request.user.vendor
#     pally_form = AddPallyForm(request.POST or None, request.FILES or None)
#     if request.method == 'POST':
#         if pally_form.is_valid():
#             new_pally = pally_form.save(commit=False)
#             new_pally.vendor = vendor
#             new_pally.save()
#             pally_form.save_m2m()

#         return redirect('vendor:pallys')

#     return render(request, 'vendor/pally-edit.html', {'form':pally_form})

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def delete_product(request, product_id):
    vendor = request.user.vendor
    products = vendor.store_product_related.all()
    product = get_object_or_404(products, id = product_id)
    product.delete()

    return redirect('vendor:products')

# @login_required
# @user_passes_test(is_vendor_test, login_url='/vendor/register/')
# def delete_pally(request, pally_id):
#     vendor = request.user.vendor
#     pallys = vendor.store_pally_related.all()
#     pally = get_object_or_404(pallys, id = pally_id)
#     pally.delete()

#     return redirect('vendor:pallys')

@login_required
@user_passes_test(is_vendor_test, login_url='/vendor/register/')
def delete_vendor(request):
    pass
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import get_object_or_404, render
from .models import Category, Product, Pally

# Create your views here.
def index(request):
    products = Product.products.all()
    pallies = Pally.pallies.all()

    # Note -- Probably add pagination
    context = {
        'products': products,
        'pallies': pallies
    }
    return render(request, 'store/index.html', context=context)


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(categories=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/product_single.html', {'product': product})

def pally_detail(request, id, slug):
    # Note to self -- Pally should be active if product is still in stock, else not active
    pally = get_object_or_404(Pally, slug=slug, id=id)

    return render(request, 'store/pally_single.html', {'pally': pally})


def search_all(request):
    query = request.GET.get('q')
    if query:
        lookups= Q(title__icontains=query) | Q(description__icontains=query)
        products = Product.products.filter(lookups)
        print(products)
        pallies = Pally.pallies.filter(product__in = products)
    else:
        products = Product.products.all()
        pallies = Pally.pallies.all()

    return render(request, 'store/search-result.html', {'products':products, 'pallies':pallies})
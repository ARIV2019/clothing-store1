import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import datetime
import json
import os
from pathlib import Path

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    title = 'Константин'
    products = Product.objects.all()[:3]

    content = {
        'title': title,
        'products': products,
    }

    return render(request, 'mainapp/index.html', content)


def contact(request):
    title = 'Константин контакты'
    visit_date = datetime.datetime.now()
    locations = []
    file_path = os.path.join(BASE_DIR, 'mainapp/json/contacts.json')
    with open (file_path, encoding='utf-8') as file_contacts:
        locations = json.load(file_contacts)
    content = {'title': title, 'visit date': visit_date, 'locations': locations}
    return render(request, 'mainapp/contact.html', content)


def product(request, pk):
    title = 'продукты'
    #same_all_products = get_same_all_products(product)
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk, is_active=True),
        #'same_all_product': same_all_products,
    }
    return render(request, 'mainapp/product.html', content)


def products(request, pk=None, page=1):
    print(pk)
    title = 'Константин товар'
    links_menu = ProductCategory.objects.filter(is_active=True)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.filter(is_active=True)
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True)

        paginator = Paginator(products, 6)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category,
        }
        return render(request, 'mainapp/products_list.html', content)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)


def not_found(request, exception):

    # выборка из базыб преобразование данных и тд
    return render(request, '404.html', context={'item': 'item'}, status=404)

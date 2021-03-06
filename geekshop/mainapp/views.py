import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import datetime
import json
import os
from pathlib import Path

from basketapp.models import Basket
from mainapp.management.commands.fill_db import JSON_PATH
from mainapp.models import Product, ProductCategory
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, \
                                      category__is_active=True).order_by('price')





def get_hot_product():
    products_list = get_products()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    title = 'Константин'
    products = get_products()[:3]
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
    links_menu = get_links_menu()
    product = get_product(pk)
    content = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
    }
    return render(request, 'mainapp/product.html', content)


#@cache_page(3600)
def products(request, pk=None, page=1):
    print(pk)
    title = 'Константин товар'
    links_menu = get_links_menu()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = get_products_orederd_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

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


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)

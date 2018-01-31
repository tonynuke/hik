import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import *


# Create your views here.


def home(request):
    return render(request, 'main/landing.html')


def order(request):

    cart_id = request.session.get('cart')
    cart = Cart.objects.all().filter(id=cart_id)[0]

    return render(request, 'main/order.html',
                  {
                      'cart_sum': cart.get_price(),
                      'cart': cart,
                  })


def store(request, page=1):
    if 'cart' not in request.session:
        cart = Cart()
        cart.save()
        request.session['cart'] = cart.id

        print('Cart not in session. New id = ', cart.id)
    else:
        cart_id = request.session.get('cart')
        cart = Cart.objects.all().filter(id=cart_id)

        if cart.all().count() == 0:
            cart = Cart()
            cart.save()
            request.session['cart'] = cart.id

        else:
            cart = cart.all()[0]

        print('Cart in session. Id = ', cart.id)

    return render(request, 'main/store.html',
                  {
                      'cart_sum': cart.get_price(),
                      'items': get_items(request, page),
                      'cart': cart.cart_items.all(),
                      'page': page,
                  })


def get_items(request, page):
    cart_id = request.session.get('cart')
    cart = Cart.objects.all().filter(id=cart_id)[0]

    items = Item.objects.all()

    paginator = Paginator(items, 2)

    cart_items = cart.cart_items.all()

    ci = []

    for item in paginator.page(page):

        quantity = 0

        ordered_item = cart_items.filter(item_id=item.id).all()
        if ordered_item.count() != 0:
            quantity = ordered_item[0].quantity

        ci.append(CartItem(item=item, quantity=quantity))

    return ci


@require_http_methods(["POST"])
def add_item(request):
    print(request.body)
    cart_id = request.session.get('cart')
    cart = Cart.objects.all().filter(id=cart_id)[0]

    request_body = json.loads(request.body.decode("utf-8"))

    cart_item = cart.cart_items.filter(item_id=request_body['id'])

    if cart_item.all().count() == 0:
        cart_item = CartItem.objects.create(item_id=request_body['id'], quantity=1)
        cart.cart_items.add(cart_item)
        cart.save()

        quantity = 1

        price = cart_item.get_price()

    else:
        tmp = cart_item.all()[0]
        tmp.quantity += 1
        tmp.save()

        quantity = tmp.quantity

        price = tmp.get_price()

    print('add item')

    response_data = {
        'cart': cart.get_price(),
        'id': request_body['id'],
        'quantity': quantity,
        'price': price
    }

    return JsonResponse(response_data, content_type='application/json')


@require_http_methods(["POST"])
def remove_item(request):
    print(request.body)
    cart_id = request.session.get('cart')
    cart = Cart.objects.all().filter(id=cart_id)[0]

    request_body = json.loads(request.body.decode("utf-8"))

    cart_item = cart.cart_items.filter(item_id=request_body['id'])

    quantity = 0
    price = 0

    if cart_item.all().count() != 0:
        tmp = cart_item.all()[0]
        tmp.quantity -= 1
        tmp.save()

        quantity = tmp.quantity

        price = tmp.get_price()

        if tmp.quantity <= 0:
            tmp = cart_item.all()[0]
            tmp.delete()

            quantity = 0

    print('remove item')

    response_data = {
        'cart': cart.get_price(),
        'id': request_body['id'],
        'quantity': quantity,
        'price': price
    }

    return JsonResponse(response_data, content_type='application/json')


@require_http_methods(["POST"])
def create_order(request):
    return JsonResponse({}, content_type='application/json')
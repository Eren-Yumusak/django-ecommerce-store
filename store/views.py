from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt


def store(request):
    data = cartData(request)
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': data['cartItems'],
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    context = {
        'items': data['items'],
        'order': data['order'],
        'cartItems': data['cartItems'],
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    context = {
        'items': data['items'],
        'order': data['order'],
        'cartItems': data['cartItems'],
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    data = json.loads(request.body.decode('utf-8')) if request.body else {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order = cartData(request)['order']
    else:
        customer, order = guestOrder(request, data)

    transaction_id = data.get('transaction_id')
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )


    return JsonResponse({'status': 'completed'}, safe=False)
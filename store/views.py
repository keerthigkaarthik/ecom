from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        cus = request.user.customer
        order, created = Order.objects.get_or_create(customer=cus, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order_total_price': 0, 'order_total_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        cus = request.user.customer
        order, created = Order.objects.get_or_create(customer=cus, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order_total_price': 0, 'order_total_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    cus = request.user.customer
    product = Product.objects.get(id=productID)

    order, created = Order.objects.get_or_create(customer=cus, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'increase':
        orderItem.quantity += 1
    elif action == 'decrease':
        orderItem.quantity -= 1
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('', safe=False)
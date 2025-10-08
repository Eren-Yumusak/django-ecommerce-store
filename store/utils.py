import json
from .models import Product, Order, OrderItem, Customer

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except Exception:
        cart = {}

    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'shipping': False,
    }

    for product_id, entry in cart.items():
        try:
            quantity = entry.get('quantity', 0)
            if quantity <= 0:
                continue
            product = Product.objects.get(id=product_id)
            total = product.price * quantity
            order['get_cart_total'] += total
            order['get_cart_items'] += quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'get_total': total,
            })
            if getattr(product, 'digital', False) is False:
                order['shipping'] = True
        except Product.DoesNotExist:
            continue

    return {'items': items, 'order': order, 'cartItems': order['get_cart_items']}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        return {'items': items, 'order': order, 'cartItems': cartItems}
    return cookieCart(request)

def guestOrder(request, data):
    # data = json payload (e.g., from checkout form) if needed
    name = data.get('form', {}).get('name', 'Guest')
    email = data.get('form', {}).get('email', '')
    cart = cookieCart(request)

    customer, _ = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)
    for item in cart['items']:
        OrderItem.objects.create(
            product=item['product'],
            order=order,
            quantity=item['quantity']
        )
    return customer, order

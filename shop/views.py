from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from decimal import Decimal

# Create your views here.

# Landing page
def home(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'products': products})


# Stores page
def stores_list(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores': stores})


def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all()
    return render(request, 'store_detail.html', {'store': store, 'products': products})


@login_required
def seller_panel(request):
    seller, created = SellerProfile.objects.get_or_create(user=request.user)
    stores = Store.objects.filter(owner=seller)
    return render(request, 'seller_panel.html', {'stores': stores})


@login_required
def customer_panel(request):
    customer, created = CustomerProfile.objects.get_or_create(user=request.user)
    return render(request, 'customer_panel.html', {'customer': customer})


@login_required
def cart_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product, customer=customer)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


@login_required
def payment(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        customer.balance += amount
        customer.save()
        return redirect('customer_panel')
    return render(request, 'payment.html')



@login_required
def checkout(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    total = sum(item.total_price() for item in cart_items)

    if customer.balance >= total and total > 0:
        customer.balance -= total
        customer.save()

        order = Order.objects.create(customer=customer, total_amount=total)

        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            seller = item.product.store.owner
            seller.store_balance += item.total_price()
            seller.save()

            item.delete()

        return render(request, 'checkout_success.html', {'order': order})
    else:
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'error': 'موجودی کافی نیست'})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
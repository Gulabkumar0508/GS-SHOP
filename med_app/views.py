from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .models import Category, Sub_Category,Product, Usercreationform,contact , orders,brand
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

def base(request):
    return render(request, 'base.html')



def index(request):
    category = Category.objects.all()
    brands = brand.objects.all()
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')

    if category_id:
        product = Product.objects.filter(sub_category=category_id).order_by('-id')
    elif brand_id:
        product = Product.objects.filter(brand=brand_id).order_by('-id')
    else:
        product = Product.objects.all()


    paginator = Paginator(product, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'product': page_obj,
        'category': category,
        'brands': brands,
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = Usercreationform(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            if new_user is not None:
                login(request, new_user)
                return redirect('index')
    else:
        form = Usercreationform()

    context = {
        'form': form
    }
    return render(request, 'signup.html', context)

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    if product.available == 'out of stock':
        messages.error(request, 'This product is out of stock and cannot be added to the cart.')
    else:
        cart.add(product=product)
        return redirect("index")
    return redirect("product_detail", id=id)


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)

    product_id_str = str(product.id)

    if product_id_str in cart.cart:
        current_quantity = cart.cart[product_id_str]['quantity']
        if current_quantity > 1:
            cart.decrement(product=product)
        else:
            cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contacts = contact(name=name, email=email, subject=subject, message=message)
        contacts.save()
        return redirect('index')
    return render(request, 'contact_us.html')

@login_required(login_url="/accounts/login/")
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        if not cart:
            return redirect('cart')

        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)
        for i in cart:
            print(i)
            price = float(cart[i]['price'])
            quantity = int(cart[i]['quantity'])
            total = price * quantity
            Order = orders(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                Quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,
                total=total
            )
            Order.save()
        request.session['cart'] = {}
        return redirect('index')


@login_required(login_url="/accounts/login/")
def your_order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    Order = orders.objects.filter(user=user)
    context = {
        'order': Order,
    }
    return render(request,'order.html',context)

def product_page(request):
    category = Category.objects.all()
    brands = brand.objects.all()
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')

    if category_id:
        product_list = Product.objects.filter(sub_category=category_id).order_by('-id')
    elif brand_id:
        product_list = Product.objects.filter(brand=brand_id).order_by('-id')
    else:
        product_list = Product.objects.all()


    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'product': page_obj,
        'category': category,
        'brands': brands,
    }
    return render(request, 'product.html', context)



def product_detail(request,id):
    product = Product.objects.filter(id = id).first()

    data = {
        'product': product,
    }
    return render(request,'product_detail.html',data)




def search_product(request):
    query = request.POST.get('query', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()

    data = {
        'products': products,
        'query': query,
    }
    return render(request, 'search.html', data)




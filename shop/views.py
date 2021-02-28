import string

import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from shop.cart import Cart
from shop.forms import OrderCreateForm, CartAddProductForm, CouponApplyForm, \
    UserRegistrationForm
from shop.models import Category, Product, OrderItem, Coupon, Order
from shop.emails import send_order_creat_email


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {'category': category,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = request.user
            order.order_number = get_random_string(10,
                                                   allowed_chars=string.ascii_uppercase + string.digits)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            send_order_creat_email(order)
            return render(request,
                          'order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'order/create.html',
                  {'cart': cart, 'form': form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        messages.info(request,
                      _("You have added {} to your cart.").format(product))
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request,
                  _("You have removed {} from your cart.").format(product))
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html',
                  {'cart': cart, 'coupon_apply_form': coupon_apply_form, })


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
            messages.info(request,
                          _("Coupon with code {} has been applied.").format(
                              code))
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.info(request,
                          _("Coupon with code {} doesn't exists.").format(
                              code))
    return redirect('shop:cart_detail')


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    html = render_to_string('order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.pk)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATICFILES_DIRS[
                                                   0] + '/css/pdf.css')])
    return response

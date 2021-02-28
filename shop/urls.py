from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/',
         views.cart_add,
         name='cart_add'),
    path('cart/remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
    path('coupon/apply/', views.coupon_apply, name='coupon_apply'),
    path('order/create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]

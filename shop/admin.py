from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin

from shop.models import Category, Product, OrderItem, Order, Coupon


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    search_fields = ('translations__name',)
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    search_fields = ('translations__name',)
    fieldsets = (
        (_("Translatable Fields"), {
            'fields': ('name', 'slug', 'description',)
        }),
        (None, {
            'fields': ('category', 'price', 'image', 'available',),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('shop:admin_order_pdf', args=[obj.pk])))


order_pdf.short_description = _('Generate invoice')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']


admin.site.register(Coupon, CouponAdmin)

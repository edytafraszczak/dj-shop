from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields, TranslatableModel


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200,
                              db_index=True, verbose_name=_('Name')),
        slug=models.SlugField(max_length=200,
                              db_index=True,
                              unique=True, verbose_name=_('Slug'))
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(TranslatableModel):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.PROTECT,
                                 verbose_name=_('Category'))

    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True, verbose_name=_('Image'))

    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name=_('Price'))
    available = models.BooleanField(default=True, verbose_name=_('Available'))
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True,
                              verbose_name=_('Name')),
        slug=models.SlugField(max_length=200, db_index=True,
                              verbose_name=_('Slug')),
        description=models.TextField(blank=True, verbose_name=_('Description'))
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT,
                                primary_key=True, verbose_name=_('User'))
    first_name = models.CharField(_('First name'), max_length=50)
    last_name = models.CharField(_('Last name'), max_length=50)
    email = models.EmailField(_('E-mail'))
    address = models.CharField(_('Address'), max_length=250)
    postal_code = models.CharField(_('Postal code'), max_length=20)
    city = models.CharField(_('City'), max_length=100)

    paid = models.BooleanField(default=False, verbose_name=_('Paid'),
                               editable=False)
    order_number = models.CharField(_('Order number'), max_length=100,
                                    unique=True, null=False, editable=False)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order {self.pk}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE,
                              verbose_name=_('Order'))
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE,
                                verbose_name=_('Product'))
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name=_('Price'))
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name=_('Quantity'))

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity

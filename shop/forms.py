from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from shop.models import Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'),
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Passwords don\'t match.'))
        return cd['password2']


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('postal_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),

            Submit('submit', _("Place order"),
                   css_class='btn btn-dark rounded-pill py-2 btn-block')
        )


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 15)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int, widget=forms.Select(
            attrs={'class': 'form-control'}))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'), widget=forms.TextInput(
        attrs={'placeholder': _('Apply a coupon'),
               'class': 'form-control border-0'}))

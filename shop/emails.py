from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


def send_order_creat_email(order):
    subject = _('Order nr. {}'.format(order.order_number))
    message = _('Dear {},\n\nYou have successfully placed an order.\
                  Your order id is {}.'.format(order.first_name,
                                               order.order_number))
    mail_sent = send_mail(subject,
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [order.email])
    return mail_sent

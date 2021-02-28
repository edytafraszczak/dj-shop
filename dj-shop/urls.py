from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from shop.views import register

admin.site.site_header = _('Django Shop Admin')
admin.site.site_title = _('Django Shop Admin')
admin.site.index_title = _("Welcome to {}".format(_('Django Shop Admin')))

urlpatterns = i18n_patterns(
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    path('account/register/', register, name='register'),
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password urls
    path('account/password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('account/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # reset password urls
    path('account/password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('account/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('', include('shop.urls', namespace='shop')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

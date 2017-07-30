from django.conf.urls import url, include

from authemail.views import (Signup, SignupVerify, Login, Logout,
                             PasswordReset, PasswordResetVerify,
                             PasswordResetVerified, PasswordChange, UserMe)

from .views import CustomLogin

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^signup/$', Signup.as_view(), name='authemail-signup'),
    url(r'^signup/verify/$', SignupVerify.as_view(),
        name='authemail-signup-verify'),

    url(r'^login/$', CustomLogin.as_view(), name='authemail-login'),
    url(r'^logout/$', Logout.as_view(), name='authemail-logout'),

    url(r'^password/reset/$', PasswordReset.as_view(),
        name='authemail-password-reset'),
    url(r'^password/reset/verify/$', PasswordResetVerify.as_view(),
        name='authemail-password-reset-verify'),
    url(r'^password/reset/verified/$', PasswordResetVerified.as_view(),
        name='authemail-password-reset-verified'),
    url(r'^password/change/$', PasswordChange.as_view(),
        name='authemail-password-change'),

    url(r'^users/me/$', UserMe.as_view(), name='authemail-me'),
]
from django.conf.urls import url, include

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^account/', include('api.accounts.urls')),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
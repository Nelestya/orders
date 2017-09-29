from django.conf.urls import url
from .views import Order_Create


urlpatterns = [
    url(r'^create/$', Order_Create.as_view(), name='order_create'),
]
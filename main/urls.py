from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^store/(?P<page>\d+)/$', store, name='store'),
    url(r'^order/$', order, name='order'),
    url(r'^create_order/$', create_order, name='create_order/'),
    url(r'^add_item_to_cart/$', add_item, name='add_item_to_cart/'),
    url(r'^remove_cart_item/$', remove_item, name='remove_cart_item/'),
]
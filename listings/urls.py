from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import post_item, my_listings, listings, item_detail, bridge_page, item_edit, item_delete,search

urlpatterns = [
    path('create/', post_item, name='post_item'),
    path('myListings/', my_listings, name='my_listings'),
    path('', listings, name='listings'),
    path('<int:item_id>/', item_detail, name='item_detail'),
    path('bridge_page/', bridge_page, name='bridge_page'),
    path('item_edit/<int:item_id>/', item_edit, name='item_edit'),
    path('item_delete/<int:item_id>/', item_delete, name='item_delete'),
    path('search/', search, name='search'),
]
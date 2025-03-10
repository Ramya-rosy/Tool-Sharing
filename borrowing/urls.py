from django.urls import path

from .views import (item_request, item_request_approve, item_request_reject, item_request_cancel, item_return,
                    item_return_confirm, item_return_override)

urlpatterns = [
    path('request/<int:item_id>/', item_request, name='item_request'),
    path('approve/<int:borrow_id>/', item_request_approve, name='item_request_approve'),
    path('reject/<int:borrow_id>/', item_request_reject, name='item_request_reject'),
    path('cancel/<int:borrow_id>/', item_request_cancel, name='item_request_cancel'),
    path('return/<int:borrow_id>/', item_return, name='item_return'),
    path('return/confirm/<int:borrow_id>/', item_return_confirm, name='item_return_confirm'),
    path('return/override/<int:borrow_id>/', item_return_override, name='item_return_override')
]

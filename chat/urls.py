from django.urls import path
from . import views

urlpatterns = [
    path('chatroom/<int:recipient_id>/', views.chat_room, name='chat_room'),
    path('send/', views.send_message, name='send_message'),
    #  path('room/', views.chat_roomi, name='chat_room_no_id'),
]
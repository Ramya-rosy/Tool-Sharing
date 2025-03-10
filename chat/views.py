# from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()

@login_required
def chat_room(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    chat, created = Chat.objects.get_or_create(
        user1=min(request.user, recipient, key=lambda x: x.pk),
        user2=max(request.user, recipient, key=lambda x: x.pk)
    )
    messages = chat.messages.order_by('timestamp')
    return render(request, 'chat/chatroom.html', {'recipient': recipient, 'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        content = request.POST.get('content')
        recipient = get_object_or_404(User, pk=recipient_id)
        chat, created = Chat.objects.get_or_create(
            user1=min(request.user, recipient, key=lambda x: x.pk),
            user2=max(request.user, recipient, key=lambda x: x.pk)
        )
        message = Message.objects.create(chat=chat, sender=request.user, receiver=recipient, content=content)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

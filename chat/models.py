from django.conf import settings
from django.db import models
from users.models import User

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} in chat {self.chat.id}"
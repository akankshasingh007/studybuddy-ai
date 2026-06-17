from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    MODE_CHOICES = [
        ('summary', 'Summary'),
        ('flashcards', 'Flashcards'),
        ('quiz', 'Quiz'),
        ('explain', 'Explain'),
        ('chat', 'Chat With Notes'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200, blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.mode} — {self.created_at:%d %b %Y}"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    user_input = models.TextField()       # PDF text or typed topic
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
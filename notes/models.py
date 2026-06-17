from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_pdf(self):
        return bool(self.file and str(self.file).lower().endswith('.pdf'))

    @property
    def is_uploaded(self):
        return bool(self.file)

    @property
    def source_label(self):
        return 'Uploaded note' if self.is_uploaded else 'Written note'

    @property
    def preview(self):
        if not self.content:
            return 'No extracted text yet.'
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

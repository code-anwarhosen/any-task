from django.db import models
from django.contrib.auth.models import User
import uuid

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=400)
    is_complete = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = str(uuid.uuid4())
        return super().save(*args, **kwargs)
    class Meta:
        ordering = ['created_at']
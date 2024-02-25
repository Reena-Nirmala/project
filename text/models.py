

from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone


class TextSummary(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    generated_summary = models.TextField()
    user1 = models.IntegerField(default=0)

    # created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f'Summary for {self.user1}'

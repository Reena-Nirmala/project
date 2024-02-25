from django.conf import settings
from django.db import models
# from django.contrib.auth.models import User
from login.models import User
from django.utils import timezone


class GrammarCheck(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    corrected_text = models.TextField()
    user1 = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    # created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'Grammar for {self.user1}'

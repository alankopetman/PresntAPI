from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pid = models.CharField(
        max_length=7,
        validators=[MinLengthValidator(7)],
        default="0000000",
    )
    is_professor = models.BooleanField(default=False)
    profile_image = models.ImageField(blank=True)

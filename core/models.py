import os
from django.db import models
from django.contrib.auth.models import User


def user_model_directory_path(instance, filename):
    # instance.__class__.__name__.lower() → "skintone" or "clothingitem"
    folder = instance.__class__.__name__.lower()
    return os.path.join(
        f"user_{instance.user.username}",
        folder,
        filename
    )

class SkinTone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_model_directory_path)
    color_hex = models.CharField(max_length=7, blank=True)

    class Meta:
        ordering = ['-user']
        indexes = [
            models.Index(fields=['-user']),
        ]

    def __str__(self):
        return f"{self.user.username}'s skin tone"


class ClothingItem(models.Model):
    class Category(models.TextChoices):
        ACCESSORY = 'accessory', 'Accessory'
        TOP  = 'top',  'Top'
        LEGS  = 'legs',  'Legs'
        FEET  = 'feet',  'Feet'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_model_directory_path)
    category = models.CharField(max_length=10, choices=Category)
    color_hex = models.CharField(max_length=7, blank=True)

    class Meta:
        ordering = ['-user']
        indexes = [
            models.Index(fields=['-user']),
        ]

    def __str__(self):
        return f"{self.category} for {self.user.username}"

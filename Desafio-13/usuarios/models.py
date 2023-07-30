import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    image = models.ImageField(upload_to='users', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_colaborador = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def assign_default_image(sender, instance, **kwargs):
    if not instance.image:
        instance.image = 'perfil-default.png'  
        instance.save()


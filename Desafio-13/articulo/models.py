from django.db import models
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Articles(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/images')
    date_published = models.DateField(default=datetime.date.today)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)  

    def __str__(self):
        return self.title

# Señal para eliminar el archivo de imagen cuando se elimina un artículo
@receiver(post_delete, sender=Articles)
def delete_article_image(sender, instance, **kwargs):
    # Eliminar el archivo de imagen cuando se elimina el artículo
    instance.image.delete(False)

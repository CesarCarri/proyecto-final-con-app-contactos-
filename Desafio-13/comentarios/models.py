from django.db import models
from articulo.models import Articles
from django.contrib.auth import get_user_model

class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"


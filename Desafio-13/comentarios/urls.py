from django.urls import path
from .views import CommentUpdateView, CommentDeleteView

app_name = 'comentarios'

urlpatterns = [
    path('editar/<int:comment_id>/', CommentUpdateView.as_view(), name='update_comment'),
    path('eliminar/<int:comment_id>/', CommentDeleteView.as_view(), name='delete_comment'),
]
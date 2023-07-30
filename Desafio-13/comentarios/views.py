from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comentarios/comment_user/comment_update.html'
    pk_url_kwarg = 'comment_id'

    def form_valid(self, form):
        form.save()
        return redirect('articulos:detail_article', post_id=form.instance.article.id)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comentarios/comment_user/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_id'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_colaborador or self.get_object().author == self.request.user)

    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_id)
        if self.test_func():  
            comment.delete()
        return redirect('articulos:detail_article', post_id=comment.article.pk)
        

       


from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.contrib import messages
from django.views.generic import View, UpdateView, DeleteView, ListView
from .forms import ArticleForm, CategoryForm
from .models import Articles, Category
from django.urls import reverse_lazy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from comentarios.models import Comment
from comentarios.forms import CommentForm



# -------------------------------------- SECCION DE CATEGORIAS -------------------------------------------

# para CREAR categorias / colaborador
class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_colaborador
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('usuarios:login_user')
        else:
            return redirect('usuarios:signup_user')

    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        categories = Category.objects.all()

        paginator = Paginator(categories, 5)

        page_number = request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {
            'form': form,
            'categories_page': page,  
        }
        return render(request, 'Articulos/category/category_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articulos:create_category')

        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'Articulos/category/category_create.html', context)


# para ELIMINAR categorias / colaborador
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'Articulos/category/category_delete.html'
    success_url = reverse_lazy('articulos:create_category')


#MOSTRAR TODAS las categorias
class AllCategoriaView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.annotate(count=Count('articles'))
    
        paginator = Paginator(categories, 6)

        page_number = request.GET.get('page')

        try:
            categories_page = paginator.page(page_number)
        except PageNotAnInteger:
            categories_page = paginator.page(1)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)

        context = {
            'categories_page': categories_page
        }
        return render(request, 'Articulos/category/all_category.html', context)
    

# Mostrar todos los artículos dependientes de esa categoría
class AllCategoriaArticlesView(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        try:
            category = Category.objects.get(pk=category_id)
            articles = category.articles_set.all()

            paginator = Paginator(articles, 3)

            page_number = request.GET.get('page')

            try:
                articles_page = paginator.page(page_number)
            except PageNotAnInteger:
                articles_page = paginator.page(1)
            except EmptyPage:
                articles_page = paginator.page(paginator.num_pages)

        except Category.DoesNotExist:
            articles_page = []
            category = None

        context = {
            'category': category,
            'articles_page': articles_page
        }
        return render(request, 'Articulos/category/all_category_articles.html', context)


# mostrar todos los articulos desde nav articulos
class AllArticlesView(View):
    def get(self, request, *args, **kwargs):
        articles = Articles.objects.all().order_by('-id')

        paginator = Paginator(articles, 6)

        page_number = request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {
            'page': page
        }
        return render(request, 'Articulos/profile/articles/all_articles.html', context)




# -------------------------------------- SECCION DE ARTICULOS -------------------------------------------


# para CREAR articulos / colaborador
class ArtCreateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_colaborador
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('usuarios:login_user')
        else:
            return redirect('usuarios:signup_user')

    def get(self, request, *args, **kwargs):
        form = ArticleForm(initial={'category':1})
        context = {
            'form': form
        }
        return render(request, 'Articulos/profile/articles/Art_create.html', context)
    
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                image = form.cleaned_data.get('image')
                date_published = form.cleaned_data.get('date_published')
                category = form.cleaned_data.get('category')

                if request.user.is_authenticated and request.user.is_colaborador:
                    p, created = Articles.objects.get_or_create(title=title, content=content, image=image, date_published=date_published, category=category, author=request.user)
                    p.save()
                    return redirect('home')
                else:
                    return redirect('usuarios:login_user')

        context = {}
        return render(request, 'Articulos/profile/articles/Art_create.html', context)
    

# para DETALLES de un articulos 
class ArtDetailView(View):
    def get(self, request, post_id, *args, **kwargs):
        article = get_object_or_404(Articles, pk=post_id)
        comments = Comment.objects.filter(article=article)
        form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'form': form,
        }
        return render(request, 'Articulos/profile/articles/Art_detail.html', context)

    def post(self, request, post_id, *args, **kwargs):
        article = get_object_or_404(Articles, pk=post_id)
        comments = Comment.objects.filter(article=article)
        form = CommentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            author = request.user
            Comment.objects.create(article=article, author=author, content=content)
            return redirect('articulos:detail_article', post_id=post_id)

        context = {
            'article': article,
            'comments': comments,
            'form': form,
        }
        return render(request, 'Articulos/profile/articles/Art_detail.html', context)
    
    def delete(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_id)
        post_id = comment.article.pk  
        comment.delete()
        return redirect('articulos:detail_article', post_id=post_id)    


# para ACTUALIZAR un artículo / colaborador
class ArtUpdateView(LoginRequiredMixin, UpdateView):
    model = Articles
    form_class = ArticleForm
    template_name = 'Articulos/profile/articles/Art_update.html'

    def test_func(self):
        return self.request.user.is_colaborador    
    
    def form_valid(self, form):
        messages.success(self.request, 'Los cambios se han guardado exitosamente.')
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('articulos:detail_article', kwargs={'post_id': pk})


# para ELIMINAR un artículo / colaborador
class ArtDeleteView(DeleteView):
    model = Articles
    template_name = 'Articulos/profile/articles/Art_delete.html'
    success_url = reverse_lazy('home')



    


#Mostrar acerca-de
class AllAboutView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'about/about.html', context)


#Mostrar contact
class AllContactView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'contacto/contacto.html', context)

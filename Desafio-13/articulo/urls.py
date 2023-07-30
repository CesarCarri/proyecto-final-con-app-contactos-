from django.urls import path
from .views import  ArtCreateView, AllArticlesView, AllCategoriaView,AllCategoriaArticlesView, CategoryCreateView, CategoryDeleteView, ArtDetailView, ArtUpdateView, ArtDeleteView, AllAboutView, AllContactView

app_name="articulos"

urlpatterns = [

    path('create/', ArtCreateView.as_view(), name="article_create"),

    path('all-articles/', AllArticlesView.as_view(), name="all_articles"),

    path('all-category/', AllCategoriaView.as_view(), name="all_category"),

    path('category/<int:category_id>/', AllCategoriaArticlesView.as_view(), name='all_category_articles'),

    path('create-category/', CategoryCreateView.as_view(), name="create_category"),

    path('<int:pk>/delete-category/', CategoryDeleteView.as_view(), name="delete_category"),

    path('Article/<int:post_id>/', ArtDetailView.as_view(), name="detail_article"),

    path('<int:pk>/update/', ArtUpdateView.as_view(), name="update_article"),

    path('<int:pk>/delete-article/', ArtDeleteView.as_view(), name="delete_article"),

    path('about/', AllAboutView.as_view(), name="about"),

    path('contac/', AllContactView.as_view(), name="contact")
]
from django.views.generic import View
from django.shortcuts import render
from articulo.models import Articles


class HomeView(View):
    def get(self, request, *args, **kwargs):
        articles = Articles.objects.order_by('-date_published')[:3]
        context={
            'articles': articles
        }
        return render(request, 'home.html',context)
    

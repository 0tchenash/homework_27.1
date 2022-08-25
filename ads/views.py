from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ads.models import Category, Ad
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from users.models import User

import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from hw27 import settings

# Create your views here.
def index(request):
    return JsonResponse({"status": "ok"}, status=200)

class CategoryListView(ListView):

    model = Category

    def get(self, request, *args, **kwargs):

        super().get(request, *args, **kwargs)

        list = request.GET.get('list', None)

        categories =  self.object_list.order_by('name')
        response = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

class CategoryDetailView(DetailView):

    model = Category

    def get(self, request, *args, **kwargs):

        try:
            category = self.get_object()
            response = {'id': category.id,
                        'name': category.name}
            return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
        except: 
            return JsonResponse({"status": 404}, status=404)

@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ['id', 'name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Category.objects.create(
            id=category_data['id'],
            name=category_data['name']
        )

        return JsonResponse({"id": category.id,
        "name": category.name}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['id', 'name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        
        category_data = json.loads(request.body)

        self.object.id = category_data['id']
        self.object.name = category_data['name']

        self.object.save()

        return JsonResponse({"id": self.object.id,
        "name": self.object.name}, status=201, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'success'}, status=204)

class AdListView(ListView):

    model = Ad

    def get(self, request, *args, **kwargs):

        super().get(request, *args, **kwargs)

        ads = self.object_list.select_related('author', 'category').order_by('-price')
        
        paginator = Paginator(ads, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        response = [{"id": ad.Id, 
                    "name" : ad.name,
                    "author": ad.author.username,
                    "price": ad.price,
                    "description": ad.description,
                    "image": ad.image.url if ad.image else None,
                    "is_published": ad.is_published,
                    "category": ad.category.name
                    } for ad in page_obj]
        return JsonResponse({"items": response,
                            "num_pages": page_num,
                            "total": paginator.num_pages}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

class AdDetailView(DetailView):

    model = Ad

    def get(self, request, *args, **kwargs):

        try:
            ad = self.get_object()
            response = {'id': ad.Id, 
                    'name' : ad.name,
                    'author': ad.author.username,
                    'price': ad.price,
                    'description': ad.description,
                    'image': ad.image.url if ad.image else None,
                    'is_published': ad.is_published,
                    'category': ad.category.name}
            return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
        except: 
            return JsonResponse({"status": 404}, status=404)

@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ['id', 'name', 'author', 'description', 'category', 'image', 'is_published', 'price']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad = Ad.objects.create(Id=ad_data['Id'],
                                name=ad_data['name'],
                                author_id=get_object_or_404(User, id=ad_data.get('author')),
                                price=ad_data['price'],
                                description=ad_data['description'],
                                is_published=ad_data['is_published'],
                                image=ad_data['image'],
                                category_id=get_object_or_404(Category, id=ad_data.get('category'))
        )

        return JsonResponse({'id': ad.Id, 
                            'name' : ad.name,
                            'author': ad.author,
                            'price': ad.price,
                            'description': ad.description,
                            'image': ad.image.url if ad.image else None,
                            'is_published': ad.is_published,
                            'category': ad.category}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['Id', 'name', 'author', 'description', 'category', 'image', 'is_published', 'price']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        
        ad_data = json.loads(request.body)

        self.object.Id = ad_data['Id']
        self.object.name = ad_data['name']
        self.object.author_id = ad_data['author']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.image = ad_data['image']
        self.object.is_published = ad_data['is_published']
        self.object.category_id = ad_data['category']

        self.object.save()

        return JsonResponse({"id": self.object.Id,
        "name": self.object.name}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'success'}, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
                'Id': self.object.Id,
                "name": self.object.name,
                "image": self.object.image.url if self.object.image else None}, status=200)
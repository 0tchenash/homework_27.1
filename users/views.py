
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import User, Location
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from hw27 import settings
from django.db.models import Count



# Create your views here.
class UserListView(ListView):

    model = User

    def get(self, request, *args, **kwargs):

        super().get(request, *args, **kwargs)

        users = self.object_list.select_related('location').order_by('username')
        users_ads = users.filter(ad__is_published=True).annotate(total_ads=Count('ad'))

        paginator = Paginator(users_ads, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        response = [{"id": user.id, 
                    "username" : user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    "tatal_ads": user.total_ads,
                    "location": user.location.name.split(", ")[0]
                    } for user in page_obj]
        return JsonResponse({"items": response,
                            "num_pages": page_num,
                            "total": paginator.num_pages}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

class UserDetailView(DetailView):

    model = User

    def get(self, request, *args, **kwargs):

        try:
            user = self.get_object()
            response = {"id": user.id, 
                    "username" : user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    "location": user.location.name}
            return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
        except: 
            return JsonResponse({"status": 404}, status=404)

# @method_decorator(csrf_exempt, name="dispatch")
# class AdCreateView(CreateView):
#     model = Ad
#     fields = ['id', 'name', 'author', 'description', 'category', 'image', 'is_published', 'price']

#     def post(self, request, *args, **kwargs):
#         ad_data = json.loads(request.body)
#         ad = Ad.objects.create(Id=ad_data['Id'],
#                                 name=ad_data['name'],
#                                 author_id=ad_data['author'],
#                                 price=ad_data['price'],
#                                 description=ad_data['description'],
#                                 is_published=ad_data['is_published'],
#                                 image=ad_data['image'],
#                                 category_id=ad_data['category']
#         )

#         return JsonResponse({'id': ad.Id, 
#                             'name' : ad.name,
#                             'author': ad.author,
#                             'price': ad.price,
#                             'description': ad.description,
#                             'image': ad.image.url if ad.image else None,
#                             'is_published': ad.is_published,
#                             'category': ad.category}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ['Id', 'name', 'author', 'description', 'category', 'image', 'is_published', 'price']

#     def post(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
        
#         ad_data = json.loads(request.body)

#         self.object.Id = ad_data['Id']
#         self.object.name = ad_data['name']
#         self.object.author_id = ad_data['author']
#         self.object.price = ad_data['price']
#         self.object.description = ad_data['description']
#         self.object.image = ad_data['image']
#         self.object.is_published = ad_data['is_published']
#         self.object.category_id = ad_data['category']

#         self.object.save()

#         return JsonResponse({"id": self.object.Id,
#         "name": self.object.name}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

# @method_decorator(csrf_exempt, name="dispatch")
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"

#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)

#         return JsonResponse({'status': 'success'}, status=200)
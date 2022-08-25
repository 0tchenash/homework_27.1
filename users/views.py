
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.decorators import method_decorator

from hw27 import settings
from users.models import User, Location

import json

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

@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        location_obj = Location.objects.get_or_create(name=''.join(user_data.get('location')))[0]

        user = User.objects.create(id=user_data['id'],
                                username=user_data['username'],
                                first_name=user_data['first_name'],
                                last_name=user_data['last_name'],
                                role=user_data['role'],
                                age=user_data['age'],
                                location=location_obj
        )

        return JsonResponse({'id': user.id, 
                            'username' : user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'role': user.role,
                            'age': user.age,
                            'location': user.location.name.split(', ')}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        
        user_data = json.loads(request.body)

        self.object.id = user_data['id']
        self.object.username = user_data['username']
        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.role = user_data['role']
        self.object.age = user_data['age']
        self.object.location_id = user_data['location']

        self.object.save()

        return JsonResponse({"id": self.object.id,
        "name": self.object.username}, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'success'}, status=200)
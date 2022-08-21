from django.shortcuts import render
from django.http import JsonResponse

from ads.models import Categories, Ads

import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return JsonResponse({"status": "ok"}, status=200)

@csrf_exempt
def get_cats(request):
    if request.method == "GET":
        categories = Categories.objects.all()
        response = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
    if request.method == 'POST':
        cat = json.loads(request.body)
        u = Categories(**cat)
        u.save()
        return JsonResponse({"status": "ok"}, status=200)


def get_cats_by_id(request, cid):
    if request.method == "GET":
        categories = Categories.objects.filter(id=cid)
        response = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@csrf_exempt
def get_ads(request):
    if request.method == "GET":
        ads = Ads.objects.all()
        response = [{'Id': ad.Id,
                    'name': ad.name,
                    'author': ad.author,
                    'description': ad.description,
                    'price': ad.price,
                    'address': ad.address,
                    'is_published': ad.is_published} for ad in ads]
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
    if request.method == 'POST':
        ad = json.loads(request.body)
        u = Ads(**ad)
        u.save()
        return JsonResponse({"status": "ok"}, status=200)

def get_ads_by_id(request, aid):
    if request.method == "GET":
        ads = Ads.objects.filter(Id=aid)
        response = [{'Id': ad.Id,
                    'name': ad.name,
                    'author': ad.author,
                    'description': ad.description,
                    'price': ad.price,
                    'address': ad.address,
                    'is_published': ad.is_published} for ad in ads]
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
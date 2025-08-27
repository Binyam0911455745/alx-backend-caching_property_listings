#from django.shortcuts import render

from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse

@cache_page(60 * 15)  # Caches the view for 15 minutes
def property_list(request):
    properties = Property.objects.all()
    data = list(properties.values())
    return JsonResponse(data, safe=False)
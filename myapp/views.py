from django.shortcuts import render
from .models import *

# Create your views here.
def photo_gallery(request):
    photos = Photo.objects.all()
    
    context = {'photos': photos}

    return render(request, 'home.html', context)

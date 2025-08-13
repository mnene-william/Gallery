from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PhotoForm

# Create your views here.
@login_required
def photo_gallery(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
        else:
            form = PhotoForm()

    photos = Photo.objects.all()

    context = {
        'photos': photos,
        'form': form,
    }

    return render(request, 'home.html', context)




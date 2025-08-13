from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import *
from .forms import *

# Create your views here.


def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


@login_required
def photo_gallery(request):
    form = PhotoForm()

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

@login_required
def profile_view(request):
    user_photos = request.user.photos.all()
    context = {'user': request.user, 'user_photos':user_photos}

    return render (request, 'profile.html', context)





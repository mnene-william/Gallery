from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import *
from .forms import *
from django.db.models import Q

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
    query = request.GET.get('q')

    if query:
        photos = Photo.objects.filter(
            Q(title__icontains=query) | Q(tags__icontains=query)
        ).order_by('-created_at')
    else:
        photos = Photo.objects.all().order_by('-created_at')

    context = {
        'photos': photos,
        'query': query,
    }

    return render(request, 'home.html', context)

@login_required
def profile_view(request):
    user_photos = request.user.photos.all()
    context = {'user': request.user, 'user_photos':user_photos}

    return render (request, 'profile.html', context)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
       u_form = UserUpdateForm(instance=request.user)
       p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,

    }

    return render (request, 'editprofile.html', context)


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('login')

def delete_photo(request, photo_id):
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)

        if photo.user == request.user:
            photo.delete()
            return redirect('profile')
        else:
            return redirect('profile')
        
@login_required
def photo_details(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(photo=photo, user=request.user, text=comment_text)

        return redirect('photo_detail', photo_id=photo_id)  

    is_liked = Like.objects.filter(photo=photo, user=request.user).exists()

    context = {
        'photo': photo,
        'is_liked': is_liked,
    }

    return render(request, 'myapp/photo_detail.html', context)


@login_required
def like_post(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        like, created = Like.objects.get_object_or_404(photo=photo, user=request.user)

        if not created:

            like.delete()

    return redirect('photo_detail', photo_id=photo_id)



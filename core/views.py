from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from core import get_face_dominant_color, get_clothing_dominant_color
from .forms import LoginForm, SkinToneForm, ClothingItemForm
from .models import SkinTone, ClothingItem


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required()
def dashboard(request):
    return render(request, 'core/dashboard.html')


@login_required()
def skincolor(request):
    face_photo = SkinTone.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = SkinToneForm(request.POST, request.FILES)
        if form.is_valid():
            # 1) build instance, set the user
            skin = form.save(commit=False)
            skin.user = request.user

            # 2) save to disk & DB so that skin.image.path is now valid
            skin.save()

            # 3) run face-detection/color-extraction
            skin.color_hex = get_face_dominant_color(skin.image.path)

            # 4) persist just the color change
            skin.save(update_fields=['color_hex'])

            return redirect('skincolor')
    else:
        form = SkinToneForm()
    return render(request, 'core/skincolor.html', {'form': form, 'face_photo': face_photo})


def facephoto_delete(request, id):
    face_photo = get_object_or_404(SkinTone, id=id, user=request.user)
    if request.method == 'POST':
        # delete the face photo from the database
        face_photo.delete()

        # delete the image file from the filesystem
        face_photo.image.delete(save=False)

        return redirect('skincolor')
    return render(request, 'core/crud_skincolor/confirm_delete.html', {'face_photo': face_photo})


@login_required()
def clothing(request):
    clothing_items = ClothingItem.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            cloth = form.save(commit=False)
            cloth.user = request.user

            # First save to write the file to disk
            cloth.save()

            # Now the file exists, and cloth.image.path is valid
            cloth.color_hex = get_clothing_dominant_color(cloth.image.path)

            # Save the color_hex field
            cloth.save(update_fields=['color_hex'])

            return redirect('clothing')
    else:
        form = ClothingItemForm()
    return render(request, 'core/clothing.html', {'form': form, 'clothing_items': clothing_items})


@login_required()
def clothing_delete(request, id):
    clothing_item = get_object_or_404(ClothingItem, id=id, user=request.user)
    if request.method == 'POST':
        # delete the clothing item from the database
        clothing_item.delete()

        # delete the image file from the filesystem
        clothing_item.image.delete(save=False)

        return redirect('clothing_list')
    return render(request, 'core/crud_clothes/confirm_delete.html', {'item': clothing_item})


@login_required()
def recommender(request):
    clothing_items = None
    if request.method == 'POST':
        face_photo = SkinTone.objects.filter(user=request.user).first()
        clothing_items = ClothingItem.objects.filter(user=request.user).all()

        if not face_photo or not clothing_items:
            return render(request, 'core/recommender.html', {'error': 'Please upload a face photo and clothing items first.'})

    return render(request, 'core/recommender.html', {'clothing_items': clothing_items})
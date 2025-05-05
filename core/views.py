from django.http import HttpResponse
from django.shortcuts import render, redirect
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
def upload_skincolor(request):
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

            return redirect('clothing_list')
    else:
        form = SkinToneForm()
    return render(request, 'core/upload_skincolor.html', {'form': form})


@login_required()
def upload_clothing(request):
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

            return redirect('clothing_list')
    else:
        form = ClothingItemForm()
    return render(request, 'core/upload_clothes.html', {'form': form})


@login_required()
def clothing_list(request):
    face_photo = SkinTone.objects.filter(user=request.user).first()
    clothing_items = ClothingItem.objects.filter(user=request.user).all()
    return render(request, 'core/clothing_list.html', {'face_photo': face_photo, 'clothing_items': clothing_items})
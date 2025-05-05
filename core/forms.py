from django import forms
from .models import SkinTone, ClothingItem


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SkinToneForm(forms.ModelForm):
    class Meta:
        model  = SkinTone
        fields = ['image']


class ClothingItemForm(forms.ModelForm):
    class Meta:
        model  = ClothingItem
        fields = ['image', 'category']

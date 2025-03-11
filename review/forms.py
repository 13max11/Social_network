from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    img = forms.ImageField(label="Завантажте сюди своє фото по бажанню", required=False)

    class Meta:
        model = Review
        fields = ['content', 'img']
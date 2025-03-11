from django import forms
from .models import Post, Community, Community_rule

from tinymce.widgets import TinyMCE

class PostCreationForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    community = forms.ModelChoiceField(
        queryset=Community.objects.all(), 
        required=True
    )
    image = forms.ImageField(label="Завантажте сюди своє фото по бажанню", required=False)

    class Meta:
        model = Post
        fields = ['community','title', 'content', 'image']

class CommunityCreationForm(forms.ModelForm):
    icon = forms.ImageField(label="Завантажте сюди іконку свого ком'юніті за бажанням", required=False)

    class Meta:
        model = Community
        fields = ['name','description', 'icon']
from django import forms
from .models import Post, Community, Community_rule, CommunityGroup

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
    background_image = forms.ImageField(label="Завантажте сюди шапку свого ком'юніті за бажанням", required=False)

    class Meta:
        model = Community
        fields = ['name','description', 'icon', 'background_image']

class CommunityGroupCreationForm(forms.ModelForm):
    class Meta:
        model = CommunityGroup
        fields = ['name', 'description', 'icon', 'private']
from django.forms import ModelForm, Textarea
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20, 'style': 'resize: both;'}),
        }

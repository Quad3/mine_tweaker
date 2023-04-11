from django.forms import ModelForm, Textarea
from .models import Post, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20, 'style': 'width: 100%;'}),
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

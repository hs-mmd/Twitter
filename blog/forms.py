from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm): 
    class Meta:
        model = Post
        fields = ("title", 'body', 'image','category')
        widget = {
            'title' : forms.TextInput(attrs={'class' :  'form-control'}),
            'body' : forms.Textarea(attrs={'class' :  'form-control'}),
        }

class CommentForm(forms.ModelForm): 
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body' : forms.Textarea(attrs={'class' :  'form-control', 'placeholder': 'Enter your comment'}),
        }

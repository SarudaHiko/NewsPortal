from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].help_text = 'Выберите одну или несколько'
        # self.fields['author'].help_text = "Выберите автора статьи или поста"

    class Meta:
        model = Post
        fields = ['author', 'title', 'category', 'text']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 120, 'rows': 1}),
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 8}),
        }
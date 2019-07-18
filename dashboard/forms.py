from django import forms

from . models import Post

from tinymce import TinyMCE

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Post
        fields = ('title','text')


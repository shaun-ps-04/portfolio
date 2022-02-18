from django import forms

# Custom
from .models import Post, Subscriber

# 3rd Party
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = Post
        exclude = ('slug', 'created_at', 'updated_at',) 


class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "email..."
        # self.fields["email"].widget.attrs["class"] = "input"
from django import forms
from .models import Comments

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text',]
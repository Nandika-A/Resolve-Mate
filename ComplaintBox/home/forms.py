from django import forms
from .models import Comment, TaskHistory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


NUMS= [
    ('approve', 'approve'),
    ('reject', 'reject'),

    ]
class CHOICES(forms.Form):
    NUMS = forms.CharField(widget=forms.RadioSelect(choices=NUMS))



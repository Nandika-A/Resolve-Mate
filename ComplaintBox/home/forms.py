from django import forms
from .models import Comment, TaskHistory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


'''      
class AssignWorkerForm(forms.ModelForm):
    class Meta:
        model = TaskHistory
        fields = ['assigned']
        widgets = {
            'assigned': forms.CheckboxSelectMultiple(attrs={'class': 'column-checkbox'})
        }
        labels = {
            'assigned' : 'Worker'
        }
'''
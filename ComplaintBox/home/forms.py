from django import forms
from .models import Comment, TaskHistory
 
#adding comments
class CommentForm(forms.ModelForm):
    content = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comment
        fields =['content']
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
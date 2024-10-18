from django import forms
from .models import Topic, Entry

class TopicForm (forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': 'Nome do Tópico'}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}
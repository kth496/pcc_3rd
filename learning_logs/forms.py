from django import forms


from .models import Topic, Entry


class TopicForm(forms.ModelForm): # (1)
    class Meta:
        model = Topic # (2)
        fields = ['text'] # (3)
        labels = {'text': ''} # (4)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''} # (1)
        widgets = {'text': forms.Textarea(attrs={'cols': 80})} # (2)

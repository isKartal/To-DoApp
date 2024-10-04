from django import forms
from .models import Todos

class ListForm(forms.ModelForm):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Todos
        fields = ["title", "description", "finished", "priority", "due_date"]

from django import forms
from .models import Document, Notes

class DocumentForm(forms.ModelForm):
    title = forms.CharField(required=False)
    class Meta:
        model = Document
        fields = ["title", "document"]

class NotesForm(forms.ModelForm):
    content = forms.CharField(required=True)
    class Meta:
        model = Notes
        fields = ["content"]
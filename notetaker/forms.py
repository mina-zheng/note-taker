from django import forms
from .models import Document, Notes

class DocumentForm(forms.ModelForm):
    title = forms.CharField(required=False)
    class Meta:
        model = Document
        fields = ["title", "document"]

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
            })
        }
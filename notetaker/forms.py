from django import forms
from .models import Document, Notes, Highlights, HighlightNotes

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

class HighlightsForm(forms.ModelForm):
    class Meta:
        model = Highlights
        fields = ["keywords"]

class HighlightNotesForm(forms.ModelForm):
    class Meta:
        model = HighlightNotes
        fields = ["notes"]
        widgets = {
            "notes": forms.Textarea(attrs={
            'rows':2})
        }
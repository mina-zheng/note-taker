from django.http import HttpResponse # type: ignore
from .forms import DocumentForm, NotesForm
from django.shortcuts import render # type:ignore
from .models import Document, Notes

def index(request):
    db_document = Document.objects.first()
    document_url = db_document.document.url if db_document else None
    
    doc_form = DocumentForm()
    note_form = NotesForm()

    notes = Notes.objects.all()
    if request.method == 'POST':
        if "upload" in request.POST:
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                upload = doc_form.save()
                document_url = upload.document.url
        
        elif "delete" in request.POST:
            if Document.objects.exists():
                record = Document.objects.first()
                record.delete()
            db_document = Document.objects.first()
            document_url = db_document.document.url if db_document else None
        
        elif "add-note" in request.POST:
            note_form = NotesForm(request.POST)
            if note_form.is_valid():
                note_form.save()
                note_form = NotesForm()
    return render(request, 'notetaker/index.html', {'form':doc_form,
                                                    'document_url':document_url,
                                                    'note_form':note_form,
                                                    'notes':notes})
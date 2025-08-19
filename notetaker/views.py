from django.http import HttpResponse # type: ignore
from .forms import DocumentForm, NotesForm
from django.shortcuts import render # type:ignore
from .models import Document, Notes, Highlights
import fitz
import os
from django.conf import settings # type:ignore

def index(request):
    db_document = Document.objects.first()
    document_url = db_document.document.url if db_document else None
    
    doc_form = DocumentForm()
    note_form = NotesForm()

    notes = Notes.objects.all()
    highlighted_instance = Highlights.objects.first()
    highlights = highlighted_instance.keywords

    new_doc_url = None

    if request.method == 'POST':
        if "upload" in request.POST:
            if db_document:
                doc_form = DocumentForm(request.POST, request.FILES, instance=db_document)
            else:
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
        
        elif "delete-note" in request.POST:
            note_id = request.POST.get("delete-note")
            note = Notes.objects.filter(id = note_id)
            note.delete()

        elif "highlight" in request.POST:
            form = NotesForm(request.POST)

            if form.is_valid():
                keyword = form.cleaned_data["content"]
                instance, created = Highlights.objects.get_or_create(document=db_document)
                instance.keywords.append(keyword)
                instance.save()

        
        elif "delete-highlight" in request.POST:
            deleted_keyword = request.POST.get("delete-highlight")
            highlights.remove(deleted_keyword)

            highlighted_instance.save()

        try:
            highlighted_instance = Highlights.objects.get(document=db_document)
            highlights = highlighted_instance.keywords
        except:
            highlights = []

    if db_document:
        document_path = db_document.document.path
        doc = fitz.open(document_path)

        try:
            highlight_instance = Highlights.objects.get(document=db_document)
            highlights = highlight_instance.keywords
        
        except:
            highlights = []

        for page in doc:
            for kw in highlights:
                text_instances = page.search_for(kw)
                for inst in text_instances:
                    page.add_highlight_annot(inst)

        temp_path = os.path.join(settings.MEDIA_ROOT, "temp.pdf")
        doc.save(temp_path)
        doc.close()
        new_doc_url = os.path.join(settings.MEDIA_URL, "temp.pdf")

    return render(request, 'notetaker/index.html', {'doc_form':doc_form,
                                                    'document_url':document_url,
                                                    'note_form':note_form,
                                                    'notes':notes,
                                                    'highlights':highlights,
                                                    'new_doc_url':new_doc_url})
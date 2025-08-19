from django.http import HttpResponse # type: ignore
from .forms import DocumentForm, NotesForm
from django.shortcuts import render # type:ignore
from .models import Document, Notes
import fitz
import os
from django.conf import settings # type:ignore

def index(request):
    db_document = Document.objects.first()
    document_url = db_document.document.url if db_document else None
    
    doc_form = DocumentForm()
    note_form = NotesForm()

    notes = Notes.objects.all()
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
            keyword = ""
            document_path = db_document.document.path
            name = "new_" + db_document.document.name
            new_doc_path = os.path.join(settings.MEDIA_ROOT, name)

            if os.path.exists(new_doc_path):
                doc = fitz.open(new_doc_path)
            else:
                doc = fitz.open(document_path)
            form = NotesForm(request.POST)

            if form.is_valid():
                keyword = form.cleaned_data["content"]
            for page in doc:
                text_instances = page.search_for(keyword)
                if text_instances:
                    for inst in text_instances:
                        page.add_highlight_annot(inst)
            
            temp = os.path.join(settings.MEDIA_ROOT, "temp.pdf")
            doc.save(temp)
            doc.close()

            os.replace(temp, new_doc_path)
            new_doc_url = os.path.join(settings.MEDIA_URL, name)

    return render(request, 'notetaker/index.html', {'doc_form':doc_form,
                                                    'document_url':document_url,
                                                    'note_form':note_form,
                                                    'notes':notes,
                                                    'new_doc_url':new_doc_url})
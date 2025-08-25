from django.http import HttpResponse # type: ignore
from .forms import DocumentForm, NotesForm, HighlightsForm, HighlightNotesForm
from django.shortcuts import render # type:ignore
from .models import Document, Notes, Highlights, HighlightNotes
import fitz
import os
from django.conf import settings # type:ignore

def index(request):
    db_document = Document.objects.first()
    document_url = db_document.document.url if db_document else None
    
    doc_form = DocumentForm()
    note_form = NotesForm()
    highlights_form = HighlightsForm()
    highlightnotes_form = HighlightNotesForm()

    notes = Notes.objects.all()
    try:
        highlighted_instance = Highlights.objects.get(document=db_document)
        highlights = highlighted_instance.keywords
    except:
        highlights = []

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
                note = note_form.save(commit=False) 
                note.document = db_document          
                note.save()                          
                note_form = NotesForm()
        
        elif "edit-note" in request.POST:
            note_id = request.POST.get("edit-note")
            new = request.POST.get("new-text")

            try:
                note = Notes.objects.get(id = note_id, document=db_document)
                note.content = new
                note.save()
            except:
                pass 
        
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

                notes_instance, created = HighlightNotes.objects.get_or_create(document=db_document)
                notes_instance.keyword = keyword
                notes_instance.save()

        
        elif "delete-highlight" in request.POST:
            deleted_keyword = request.POST.get("delete-highlight")
            keywords = highlighted_instance.keywords or []

            keywords.remove(deleted_keyword)
            highlighted_instance.keywords = keywords

            highlighted_instance.save()

            HighlightNotes.objects.filter(document=db_document,keyword=deleted_keyword).delete()

            


        elif "add-highlight-note" in request.POST:
            keyword = request.POST.get("add-highlight-note")
            keyword_instance, created = HighlightNotes.objects.get_or_create(document = db_document, keyword=keyword)

            form = HighlightNotesForm(request.POST, instance=keyword_instance)
            if form.is_valid():
                keyword_instance.save()
                form = HighlightNotesForm()

        elif "edit-highlight-note" in request.POST:
            keyword = request.POST.get("edit-highlight-note")
            new = request.POST.get("new-highlight")
            try:
                highlight = HighlightNotes.objects.get(keyword=keyword, document=db_document)
                highlight.notes = new
                highlight.save()
            except:
                pass 
            
        try:
            highlighted_instance = Highlights.objects.get(document=db_document)
            highlights = highlighted_instance.keywords
        except:
            highlights = []
        
    if db_document:
        document_path = db_document.document.path
        doc = fitz.open(document_path)
        tup = []

        try:
            highlight_instance = Highlights.objects.get(document=db_document)
            highlights = highlight_instance.keywords

            for keyword in highlights:
                try:
                    note_instance = HighlightNotes.objects.get(document=db_document, keyword=keyword)
                    tup.append((keyword, note_instance.notes))
                except:
                    tup.append((keyword, ""))
        except:
            highlights = []
            dict = {}

        for page in doc:
            for kw in highlights:
                text_instances = page.search_for(kw)
                for inst in text_instances:
                    page.add_highlight_annot(inst)

        name = db_document.document.name + "_new.pdf"
        temp_path = os.path.join(settings.MEDIA_ROOT, name)
        doc.save(temp_path)
        doc.close()
        new_doc_url = os.path.join(settings.MEDIA_URL, name)

    return render(request, 'notetaker/index.html', {'doc_form':doc_form,
                                                    'document_url':document_url,
                                                    'note_form':note_form,
                                                    'notes':notes,
                                                    'highlights':highlights,
                                                    'new_doc_url':new_doc_url,
                                                    'highlights_form':highlights_form,
                                                    'highlightnotes_form':highlightnotes_form,
                                                    "tup":tup})
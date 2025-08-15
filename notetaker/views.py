from django.http import HttpResponse # type: ignore
from .forms import DocumentForm
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world!")

def upload_file(request):
    form = DocumentForm()
    document_url = None
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            document_url = upload.document.url
        else:
            DocumentForm()
    
    return render(request, 'notetaker/index.html', {'form':form, 'document_url':document_url})
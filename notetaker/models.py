from django.db import models # type: ignore

class Document(models.Model):
    title = models.CharField()
    document = models.FileField(upload_to='')


from django.db import models # type: ignore
from django.contrib.postgres.fields import ArrayField # type: ignore

class Document(models.Model):
    title = models.CharField(blank=True)
    document = models.FileField(upload_to='')


class Notes(models.Model):
    content = models.CharField()

class Highlights(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    keywords = ArrayField(models.CharField(), 
                          default=list,
                          blank=True
    )
    notes = models.CharField(default="")


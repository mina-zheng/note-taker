from django.db import models # type: ignore

class Document(models.Model):
    title = models.CharField(blank=True)
    document = models.FileField(upload_to='')


class Notes(models.Model):
    content = models.CharField()

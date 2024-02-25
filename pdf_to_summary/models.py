# models.py

from django.db import models

class PdfDocument(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    # pages_to_summarize = models.IntegerField()
    pages_to_summarize = models.CharField(max_length=20)  # Change the field type to CharField

    summarized_text = models.TextField(blank=True, null=True)
    user1 = models.IntegerField(default=0)
    # created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.pdf_file.name} - Pages: {self.pages_to_summarize}"

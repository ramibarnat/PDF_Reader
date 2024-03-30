from django.db import models

class CsvData(models.Model):
    csv_file = models.BinaryField(blank=True)

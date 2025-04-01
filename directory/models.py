from django.db import models
from datetime import datetime


class TypeOperation(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=40)
    type_operation = models.ForeignKey(TypeOperation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Subcategories(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class DDS(models.Model):
    date = models.DateField(null=True, blank=True)
    summ = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(null=True)
    operation = models.ForeignKey(TypeOperation, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='category_dds')
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, related_name='subcategory_dds')

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.date.today()
        super(DDS, self).save(*args, **kwargs)
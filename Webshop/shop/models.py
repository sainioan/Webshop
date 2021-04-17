from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=5000, null=True)
    image = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.product_name
    
    def delete(self, *args, **kwargs):
        super(Products, self).delete(*args, **kwargs)


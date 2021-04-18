from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import *
from django.conf import settings
# Create your models here.

CATEGORY = (
    ('Cl', 'Clothes'),
    ('Mu', 'Music'),
    ('El', 'Electronics')
)
class Product(models.Model):

    product_name = models.CharField(max_length=100)
    # category = models.CharField(choices=CATEGORY, max_length=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=5000, null=True)
    image = models.ImageField(upload_to='upload/', null=True, blank=True)
    def __str__(self):
        return self.product_name
    
    def view_product(self):
            return reverse("shop:product", kwargs={
            "pk" : self.pk
        
    })

    def add_to_cart(self):
        return reverse("shop:add_to_cart", kwargs={
            "pk" : self.pk
        })

    def remove_from_cart(self):
        return reverse("shop:remove_from_cart", kwargs={
            "pk" : self.pk
        })
    
    def delete(self, *args, **kwargs):
        super(Products, self).delete(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateField(auto_now_add=True)

    # class Meta:
    #     verbose_name = 'Carts'
    #     verbose_name_plural = 'Carts'

    def __str__(self):
        return '%s' % (self.user_id)

    def __str__(self):
        return f"{self.count} of {self.product.product_name}"

    def get_total_amount(self):
        return self.count * self.product.price
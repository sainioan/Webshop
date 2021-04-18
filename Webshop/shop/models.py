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
    category = models.CharField(choices=CATEGORY, max_length=2, null=True)
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

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE, unique=False)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price 

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):    
        self.quantity = self.quantity + int(quantity)
        self.save() 


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem)
    count = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    date = models.DateField(auto_now_add=True)
    

    def get_total_amount(self):
        total = 0
        for pr in self.products.all():
            total += pr.price()
        return total
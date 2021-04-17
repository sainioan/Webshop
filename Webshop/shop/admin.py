from django.contrib import admin

from django.utils.safestring import mark_safe
from .models import *

class ProductAdmin(admin.ModelAdmin):
    def image_admin(self, obj):
        return mark_safe('<img src="{image}" class="img-fluid" width="20%" />'.format(image=obj.image.url))
    image_admin.short_description = 'Image'
    def name_admin(self, obj):
        return mark_safe('<a href="/product/{product_name}/" target="_blank">{product_name}</a>'.format(name=obj.name))
    name_admin.short_description = 'Product Name'
    list_display = ('image_admin', 'product_name', 'price', 'description')
    list_filter = ('price',)
    search_fields = ('product_name', )
admin.site.register(Product, ProductAdmin)
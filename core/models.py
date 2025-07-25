from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(blank=True)
    product_link = models.URLField()
    current_price = models.CharField(max_length=50)
    carton_price = models.CharField(max_length=50, blank=True)
    single_price = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100)
    item_code = models.CharField(max_length=50, blank=True)  
    supplier = models.CharField(max_length=50, blank=True) 
    supplier_url = models.CharField(max_length=50, blank=True)   

    def __str__(self):
        return f"{self.name} ({self.item_code})"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

from django.db import models

# Create your models here.
class Product(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("deleted", "Deleted"),
    ]

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
    item_body = models.CharField(max_length=500, blank=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")  

    def __str__(self):
        return f"{self.name} ({self.item_code})"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Favorites(models.Model):
    userid = models.CharField(max_length=255)
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
    item_body = models.CharField(max_length=500, blank=True)  
    item_quantity = models.IntegerField(default=1) 

    def __str__(self):
        return f"{self.username} ({self.id})"
    
#  ['id', 'username', 'password', 'email']
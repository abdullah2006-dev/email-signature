from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return f"Banner {self.id}"

       
class Signature(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    surname = models.CharField(max_length=100)  
    function = models.CharField(max_length=100, blank=True, null=True) 
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)  
    phone = models.CharField(max_length=20, blank=True, null=True)  
    email = models.EmailField()
    signature_type = models.CharField(max_length=50, blank=True, null=True)  
    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname or ''}".strip()
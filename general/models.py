from django.db import models

# Create your models here.
class ContactRequest(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    message = models.TextField()
    responded_to = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
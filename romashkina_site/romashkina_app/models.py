from django.db import models

# shop/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='img/')  # зберігаємо в медіа/img

    def __str__(self):
        return self.name

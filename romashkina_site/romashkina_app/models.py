from django.db import models

# shop/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна')
    image = models.ImageField(upload_to='img/', verbose_name='Фото')  # зберігаємо в медіа/img
    visible = models.BooleanField(default=True, verbose_name="Відображення")  # новий стовпець


    def __str__(self):
        return self.name

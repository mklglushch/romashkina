from django.contrib import admin
from .models import Product

admin.site.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_editable = ['price', "available"]
# редагування ціни одразу в адмінці
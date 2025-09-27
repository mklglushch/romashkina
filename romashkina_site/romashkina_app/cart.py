# romashkina_app/cart.py
from .models import Product

class Cart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if not cart:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        pid = str(product_id)
        if pid in self.cart:
            self.cart[pid] += quantity  # якщо товар вже в корзині — збільшуємо кількість
        else:
            self.cart[pid] = quantity  # додаємо новий товар
        self.save()

    def remove(self):
        del self.session[self.SESSION_KEY]  # Видаляємо кошик з сесії
        self.save()  # Зберігаємо зміни

    def save(self):
        self.session.modified = True  # повідомляємо Django, що сесія була змінена

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for prod in products:
            qty = self.cart[str(prod.id)]
            yield {
                'product': prod,
                'quantity': qty,
                'subtotal': prod.price * qty
            }

    def get_total_price(self):
        return sum(prod.price * qty for prod, qty in [
            (item['product'], item['quantity']) for item in self
        ])
        
    def get_total_quantity(self):
        """
        Повертає сумарну кількість одиниць товарів у корзині.
        """
        return sum(self.cart.values())
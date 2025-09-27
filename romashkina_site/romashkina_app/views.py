from django.shortcuts import render

from django.shortcuts import render
import requests

def main_page(request):
    return render(request, 'main.html')

def shop_page(request):
    return render(request, 'shop.html')

def about_page(request):
    return render(request, 'about.html')

# def contact_page(request):
#     return render(request, 'contact.html')

def test_page(request):
    return render(request, 'test.html')

TELEGRAM_TOKEN = "7739344621:AAEZmlNEIKmQgb3lZHxSi1IMmPzoNEuTV0Q"
CHAT_ID = "-4982840825"

def send_telegram_message(text: str) -> bool:

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    try:
        response = requests.post(url, data=data, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def contact_page(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName", "").strip()
        contact_method = request.POST.get("contactMethod", "").strip()
        phone = request.POST.get("phone", "").strip()

        message = (
            "Новий оптовий покупець\n"
            f"Ім'я та прізвище: {first_name}\n"
            f"Месенджер: {contact_method}\n"
            f"Телефон: {phone}"
        )

        success = send_telegram_message(message)

        if success:
            info = "Чудово! Менеджер невдовзі з вами зв*яжеться."
        else:
            info = "Сталася помилка при відправці. Спробуйте пізніше."

        return render(request, "contact.html", {"message": info})

    return render(request, "contact.html")


import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST

def create_order(request):
    try:
        # Отримуємо JSON дані з форми
        order_data = json.loads(request.POST.get('order_data', '{}'))
        
        # Вилучаємо всі необхідні дані
        delivery_data = order_data.get('delivery_data', {})
        receiver_info = order_data.get('receiver_info', {})
        products_data = order_data.get('products_data', [])
        total_price = order_data.get('total_price', '0')
        payment_method = order_data.get('payment_method', 'transfer')
        
        # Перевіряємо обов'язкові поля
        if not receiver_info.get('full_name') or not receiver_info.get('phone'):
            return JsonResponse(
                {'status': 'error', 'message': 'Не заповнені обов\'язкові поля'},
                status=400
            )
        
        # Формуємо текст повідомлення для Telegram
        message_lines = [
            "📦 НОВЕ ЗАМОВЛЕННЯ",
            "",
            f"👤 Отримувач: {receiver_info.get('full_name', '')}",
            "",
            f"📞 Телефон: {receiver_info.get('phone', '')}",
            "",
            f"🚚 Доставка: {delivery_data.get('department_name', '')}",
            "",
            f"📍 Адреса: {delivery_data.get('department_address', '')}",
            "",
            f"💳 Спосіб оплати: {'Накладений платіж' if payment_method == 'cash_on_delivery' else 'Переказ на карту'}",
            "",
            "🛒 ТОВАРИ:"
        ]
        
        # Додаємо інформацію про товари
        for product in products_data:
            message_lines.append(
                f"- {product.get('name', '')} "
                f"({product.get('quantity', '')} шт.) - "
                f"{product.get('price', '')} грн"
            )
        
        # Додаємо підсумкову інформацію
        message_lines.extend([
            "",
            f"💰 ЗАГАЛЬНА СУМА: {total_price} грн",
        ])
        
        # Об'єднуємо всі рядки повідомлення
        message = "\n".join(message_lines)
        
        # Відправляємо повідомлення в Telegram (ваша функція)
        send_telegram_message(message)
        
        # Повертаємо успішну відповідь
        return render(request, 'order_success.html', {
            'order_number': request.session.session_key[:8].upper(),
            'receiver_name': receiver_info.get('full_name')
        })
        
    except json.JSONDecodeError as e:
        return HttpResponseBadRequest("помилка 404")
    except Exception as e:
        return redirect('shop')



# romashkina_app/views.py
from django.shortcuts import render, redirect
from .models import Product
from .cart import Cart
from django.http import HttpResponseBadRequest


from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

def cart_update(request, product_id):
    cart = Cart(request)
    
    # Отримуємо значення з кнопки (+1 або -1)
    change_quantity = request.POST.get('change_quantity')

    if change_quantity is None:
        return HttpResponseBadRequest("Не вказано зміни кількості товару.")
    
    try:
        change = int(change_quantity)
    except ValueError:
        return HttpResponseBadRequest("Невірний формат зміни кількості.")
    
    # Отримуємо поточну кількість товару
    current_quantity = cart.cart.get(str(product_id), 0)
    
    # Розраховуємо нову кількість
    new_quantity = current_quantity + change
    
    # Перевіряємо, щоб кількість не була меншою за 1
    if new_quantity < 1:
        new_quantity = 1
    
    # Оновлюємо товар у корзині
    cart.add(product_id, new_quantity - current_quantity)  # передаємо різницю
    
    return redirect('cart_detail')  # Переходимо назад на сторінку корзини

def cart_clear(request):
    cart = Cart(request)
    cart.remove()  # очищаємо корзину
    return redirect('shop')  # редірект на сторінку корзини

def shop_page(request):
        products = Product.objects.all()
        cart = Cart(request)
        total_items = cart.get_total_quantity()  # нова змінна

        return render(request, 'shop.html', {
            'products': products,
            'cart_count': total_items,       # передаємо її в шаблон
        })

def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id, quantity=1)  # додаємо товар в корзину
    return redirect('shop')  # після додавання редіректимо на сторінку корзини


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {
        'cart_items': list(cart),
        'total_price': cart.get_total_price()
    })


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')  # після видалення редіректимо на сторінку корзини





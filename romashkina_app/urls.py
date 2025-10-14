# romashkina_app/urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.main_page, name='main'),          # головна сторінка
    path('shop/', views.shop_page, name='shop'),      # магазин
    path('about/', views.about_page, name='about'),   # про нас
    path('contact/', views.contact_page, name='contact'),# контакти
    path('create-order/', views.create_order, name='create_order'),
    path('cart/', views.cart_detail, name='cart_detail'),  # сторінка корзини
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),  # додавання товару
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),  # видалення товару
    path('cart/clear/', views.cart_clear, name='cart_clear'),  # очищення корзини
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),  # маршрут для оновлення кількості

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
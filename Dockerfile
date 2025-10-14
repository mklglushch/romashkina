# 1. БАЗОВИЙ ОБРАЗ
# Використовуємо повний образ для простоти
FROM python:3.11

# 2. НАЛАШТУВАННЯ СЕРЕДОВИЩА
WORKDIR /usr/src/app

# Встановлюємо необхідні системні пакети для Pillow
# (Включаємо всі можливі залежності для надійності)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev && \
    rm -rf /var/lib/apt/lists/*
    
# 3. КОД ТА ЗАЛЕЖНОСТІ
# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# 4. НАЛАШТУВАННЯ СТАТИКИ
# Встановлюємо змінну середовища для налаштувань
ENV DJANGO_SETTINGS_MODULE=romashkina_site.settings
ENV PYTHONUNBUFFERED 1

# Збираємо статичні файли (ВАЖЛИВО: цей крок відбувається лише раз під час збірки образу)
RUN python manage.py collectstatic --noinput

# 5. НАЛАШТУВАННЯ ЗАПУСКУ
EXPOSE 8000

# Команда для запуску контейнера
# (Gunicorn, 3 працівники, без тайм-ауту)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "romashkina_site.wsgi:application"]

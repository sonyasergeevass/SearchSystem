# Базовый образ с Python
FROM python:3.13-slim

# Устанавливаем зависимости для Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium \
    libnss3 \
    libgconf-2-4 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    libdrm2 \
    libgbm1 \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="$HOME/.local/bin:$PATH"

ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root

# Указываем порт
EXPOSE 8000

# Запуск сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
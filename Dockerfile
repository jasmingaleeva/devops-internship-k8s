# Использование легковесного базового образа Python
FROM python:3.12-alpine

# Настройка переменных окружения для небуферизованного вывода и порта
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_PORT=32777

# Создание непривилегированного пользователя для безопасности (non-root)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Создание рабочей директории
WORKDIR /app

# Копирование файла зависимостей и демонстрация эффективного кэширования слоев
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Копирование исходного кода приложения
COPY app/ /app/

# Переключение на непривилегированного пользователя
USER appuser

# Открытие порта 32777 согласно требованиям задания
EXPOSE 32777

# Запуск веб-приложения
ENTRYPOINT ["python", "main.py"]

# Yandex IoT Bridge для Railway

Простой API сервис для управления устройствами Яндекс умного дома через HTTP запросы.

## Развертывание на Railway

### Шаг 1: Создать новый проект на Railway

1. Зайди на https://railway.app
2. Нажми **"New Project"**
3. Выбери **"Deploy from GitHub repo"** или **"Empty Project"**

### Шаг 2: Загрузить код

**Вариант А: Через GitHub (рекомендуется)**
1. Создай новый репозиторий на GitHub
2. Загрузи туда файлы: `main.py`, `requirements.txt`, `Procfile`
3. В Railway подключи этот репозиторий

**Вариант Б: Напрямую**
1. В Railway выбери **"Deploy from local"**
2. Загрузи файлы

### Шаг 3: Настроить переменные окружения

В Railway → Settings → Variables добавь:

```
YANDEX_TOKEN=y0__xCew86dCBij9xMgz4HM8xUErWgDhQUcgJt31uQcktr3HPbT4g
DEVICE_ID=ca02d1ae-9ee6-4bdb-bba5-aa451bcd241f
```

### Шаг 4: Deploy

Railway автоматически развернет сервис. После деплоя получишь URL типа:
```
https://your-app-name.up.railway.app
```

## Использование API

### Включить розетку:
```bash
GET https://your-app-name.up.railway.app/control/on
```

### Выключить розетку:
```bash
GET https://your-app-name.up.railway.app/control/off
```

### POST запрос:
```bash
POST https://your-app-name.up.railway.app/control
Body: {"action": "on"}  # или "off"
```

### Проверка здоровья:
```bash
GET https://your-app-name.up.railway.app/health
```

## Настройка n8n

В n8n вместо прямого вызова Yandex API используй:

**Для включения:**
- Method: GET
- URL: `https://your-app-name.up.railway.app/control/on`

**Для выключения:**
- Method: GET
- URL: `https://your-app-name.up.railway.app/control/off`

Авторизация не требуется, т.к. токен уже настроен в переменных окружения Railway.

## Логи и мониторинг

Смотри логи в Railway → Deployments → View Logs

## Troubleshooting

Если не работает:
1. Проверь переменные окружения в Railway
2. Проверь логи деплоя
3. Убедись что токен Яндекса валидный
4. Проверь DEVICE_ID розетки

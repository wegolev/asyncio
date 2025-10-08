### 1. Введение и установка

**Что такое aiohttp?**
Это асинхронная библиотека для работы с HTTP в Python, построенная на asyncio. В отличие от синхронной `requests`, она позволяет не только делать запросы, но и создавать серверы, а также работать с WebSockets.

**Установка:**
```bash
pip install aiohttp
# Для работы с файлами на сервере может понадобиться:
pip install aiofiles
```

---

### 2. Создание HTTP-клиентов

#### Пример 1: Базовый GET-запрос

**Код:**
```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Статус: {response.status}")
            print(f"Тело ответа: {await response.text()}")

asyncio.run(fetch('http://httpbin.org/get'))
```

**Пояснение:**
1. `ClientSession()` — создает сессию для управления соединениями.
2. `session.get(url)` — выполняет асинхронный GET-запрос.
3. `response.text()` — асинхронно читает тело ответа (поэтому нужен `await`).
4. `async with` — асинхронный контекстный менеджер, который автоматически закрывает соединение.

**Как запустить:**
Скопируйте код в файл `client_get.py` и выполните:
```bash
python client_get.py
```

**Тест:**
Замените URL на `http://httpbin.org/get` — это тестовый сервис, который вернет ваш запрос в виде JSON.

---

#### Пример 2: POST-запрос с JSON

**Код:**
```python
import aiohttp
import asyncio

async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            print(f"Статус: {response.status}")
            print(f"Тело ответа: {await response.text()}")

data = {"ключ": "значение"}
asyncio.run(post_data('http://httpbin.org/post', data))
```

**Пояснение:**
- `json=data` — автоматически сериализует словарь в JSON и устанавливает заголовок `Content-Type: application/json`.

**Запуск:**
Сохраните как `client_post.py` и запустите.

**Тест:**
httpbin.org вернет отправленные вами данные, что подтвердит успешность запроса.

---

#### Пример 3: Запрос с таймаутом

**Код:**
```python
import aiohttp
import asyncio

async def fetch_with_timeout(url):
    timeout = aiohttp.ClientTimeout(total=2)  # Таймаут 2 секунды
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as response:
                print(f"Статус: {response.status}")
                print(f"Тело ответа: {await response.text()}")
        except asyncio.TimeoutError:
            print("Запрос превысил время ожидания")

asyncio.run(fetch_with_timeout('http://httpbin.org/delay/5'))  # Сервер ждет 5 секунд
```

**Пояснение:**
- `ClientTimeout(total=2)` — устанавливает общий таймаут 2 секунды.
- Сервер `httpbin.org/delay/5` искусственно задерживает ответ на 5 секунд, поэтому наш запрос с таймаутом в 2 секунды завершится ошибкой.

**Тест:**
Запустите код и убедитесь, что через 2 секунды выводится сообщение о таймауте.

---

### 3. Асинхронный HTTP-сервер

#### Пример 1: Простой сервер

**Код (server_simple.py):**
```python
from aiohttp import web

async def handle(request):
    return web.Response(text="Hello, World!")

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
```

**Пояснение:**
1. Создаем приложение `web.Application()`.
2. Добавляем маршрут: `web.get('/', handle)` — для GET-запросов к корню.
3. `web.run_app(app)` — запускает сервер.

**Запуск:**
```bash
python server_simple.py
```
**Тест:**
Откройте в браузере `http://127.0.0.1:8080/` — увидите "Hello, World!".

---

#### Пример 2: Сервер с загрузкой файлов

**Код (server_files.py):**
```python
from aiohttp import web
import aiofiles
import os

async def handle_upload_file(request):
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == 'file'
    filename = field.filename

    # Сохранение файла на диск
    size = 0
    async with aiofiles.open(os.path.join('uploads', filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            await f.write(chunk)
    return web.json_response({'filename': filename, 'size': size})

app = web.Application()
app.add_routes([web.post('/upload', handle_upload_file)])

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    web.run_app(app, host='127.0.0.1', port=8080)
```

**Пояснение:**
- `request.multipart()` — используется для обработки данных формы, включая файлы.
- `aiofiles` — библиотека для асинхронной работы с файлами.

**Запуск:**
Убедитесь, что установлен `aiofiles`, затем запустите сервер.

**Тест:**
Создайте HTML-форму или используйте `curl`:
```bash
curl -X POST -F "file=@./test.txt" http://127.0.0.1:8080/upload
```
Файл `test.txt` должен появиться в папке `uploads`.

---

### 4. Работа с WebSocket

#### Пример: Эхо-сервер и клиент

**Сервер (server_ws.py):**
```python
from aiohttp import web

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(f"Message received: {msg.data}")
        elif msg.type == web.WSMsgType.ERROR:
            print(f'WebSocket error: {ws.exception()}')

    return ws

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
```

**Клиент (client_ws.py):**
```python
import aiohttp
import asyncio

async def websocket_client():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:8080/ws') as ws:
            await ws.send_str("Hello, server")
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f"Message from server: {msg.data}")
                    await ws.close()
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f'WebSocket error: {ws.exception()}')
                    break

asyncio.run(websocket_client())
```

**Пояснение:**
- Сервер принимает соединение, читает сообщения и отправляет их обратно с префиксом.
- Клиент подключается, отправляет сообщение и печатает ответ.

**Запуск:**
1. Запустите сервер: `python server_ws.py`
2. В другом терминале запустите клиент: `python client_ws.py`

**Тест:**
Клиент должен получить ответ: `Message from server: Message received: Hello, server`.

---

### Итог

Вы изучили основы aiohttp:
- **Клиенты:** GET/POST-запросы, таймауты, заголовки.
- **Серверы:** обработка маршрутов, JSON, файлы.
- **WebSockets:** простой эхо-сервер и клиент.

Для тестирования серверов можно использовать:
- Браузер (для GET)
- `curl` (для POST/upload)
- Написанные клиенты (для WebSockets)
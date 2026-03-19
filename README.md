# BFU Electronics ESP32 Wi-Fi LCD Control Panel

Проєкт на **ESP32 + LCD 1602 I2C**, який:
- підключається до Wi‑Fi
- показує статус на LCD екрані
- запускає локальний вебсервер
- дозволяє **вмикати / вимикати LED**
- дозволяє **перемикати мову сторінки**
- дозволяє **перемикати світлу / темну тему**
- використовує **buzzer** для звукового підтвердження дій

---

## Можлива назва репозиторію

**bfu-esp32-wifi-lcd-control**

Інші хороші варіанти:
- `esp32-lcd-web-control`
- `bfu-electronics-esp32-control-panel`
- `esp32-i2c-lcd-led-webserver`

---

## Що є в проєкті

Файли:
- `main.py` — основна логіка проєкту
- `i2c_lcd.py` — драйвер LCD по I2C
- `lcd_api.py` — базовий LCD API

---

## Що потрібно для роботи

### Обладнання
- ESP32
- LCD 1602 з I2C модулем
- LED
- резистор для LED
- buzzer
- дроти
- USB кабель
- Wi‑Fi мережа 2.4 GHz

### Програми
- Thonny / uPyCraft / ampy / rshell
- MicroPython firmware для ESP32

---

## Схема підключення

### LCD 1602 I2C -> ESP32
- **SDA** -> `GPIO21`
- **SCL** -> `GPIO22`
- **VCC** -> `5V` або `3.3V` залежно від модуля
- **GND** -> `GND`

### LED -> ESP32
- **LED signal** -> `GPIO2`
- другий контакт LED -> через резистор на `GND`

### Buzzer -> ESP32
- **Buzzer signal** -> `GPIO27`
- **GND** -> `GND`

> У коді саме такі піни: LCD через `GPIO21/GPIO22`, LED на `GPIO2`, buzzer на `GPIO27`.

---

## Важливо перед завантаженням на GitHub

У твоєму `main.py` зараз записані реальні дані Wi‑Fi:
```python
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'
```

### Правильно зробити так:
1. **не викладати реальний пароль у GitHub**
2. перед публікацією замінити свої дані на шаблон:
```python
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'
```

Якщо пароль уже десь світився — краще потім змінити пароль Wi‑Fi.

---

## Як прошити ESP32

1. Підключи ESP32 до комп’ютера через USB
2. Відкрий **Thonny**
3. Обери:
   - **Tools**
   - **Options**
   - **Interpreter**
   - **MicroPython (ESP32)**
4. Якщо прошивка ще не встановлена — спочатку встанови MicroPython firmware
5. Після підключення ESP32 відкрий файли:
   - `main.py`
   - `i2c_lcd.py`
   - `lcd_api.py`
6. Завантаж їх на плату:
   - `main.py` -> у корінь пристрою
   - `i2c_lcd.py` -> у корінь пристрою
   - `lcd_api.py` -> у корінь пристрою

---

## Як запустити

1. У `main.py` встав свою назву Wi‑Fi мережі:
```python
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'
```

2. Збережи файл на ESP32 як `main.py`

3. Перезапусти плату

4. Після запуску:
- LCD покаже boot sequence
- ESP32 підключиться до Wi‑Fi
- отримає IP адресу
- запустить вебсервер на **порті 80**

5. Після цього у браузері відкрий:
```text
http://IP_АДРЕСА_ESP32
```

Наприклад:
```text
http://192.168.1.55
```

---

## Як дізнатись IP адресу

Після підключення до Wi‑Fi:
- IP з’явиться в консолі
- IP також показується на LCD

У коді це робиться так:
```python
ip = wifi.ifconfig()[0]
print("IP:", ip)
```

---

## Що вміє вебпанель

Через браузер ти можеш:
- увімкнути LED
- вимкнути LED
- перемкнути мову:
  - English
  - Українська
- перемкнути тему:
  - Light
  - Dark

---

## Як працює логіка

### Під час запуску
- ініціалізується LED
- ініціалізується buzzer
- сканується I2C
- шукається LCD за адресами:
  - `0x27`
  - `0x3F`

Якщо LCD не знайдений:
```python
raise Exception("LCD not found. Check SDA / SCL / VCC / GND")
```

### Далі
- запускається boot animation
- ESP32 підключається до Wi‑Fi
- створюється socket server
- браузерні запити обробляються через прості URL:
  - `/on`
  - `/off`
  - `/lang/en`
  - `/lang/ua`
  - `/theme/light`
  - `/theme/dark`

---

## Якщо LCD не працює

Перевір:
- SDA справді на `GPIO21`
- SCL справді на `GPIO22`
- є живлення
- правильна I2C адреса модуля
- чи бачить ESP32 дисплей у `i2c.scan()`

У консолі має вивести щось типу:
```python
I2C devices: [39]
```

`39` — це `0x27`

---

## Якщо Wi‑Fi не підключається

Перевір:
- правильність `ssid`
- правильність `password`
- мережа саме **2.4 GHz**
- сигнал достатньо сильний
- роутер не блокує пристрій

У коді таймаут підключення приблизно 18 секунд.

---

## Рекомендована структура репозиторію

```text
bfu-esp32-wifi-lcd-control/
│
├── main.py
├── i2c_lcd.py
├── lcd_api.py
├── README.md
└── .gitignore
```

---

## Приклад .gitignore

```gitignore
__pycache__/
*.mpy
.DS_Store
Thumbs.db
```

---

## Як створити репозиторій на GitHub

1. Зайди на GitHub
2. Натисни **New repository**
3. В полі **Repository name** введи:
```text
bfu-esp32-wifi-lcd-control
```

4. В полі **Description** можеш вставити:
```text
ESP32 Wi-Fi control panel with LCD 1602 I2C, LED, buzzer and web interface.
```

5. Обери:
- **Public** або **Private**
- постав галочку **Add a README file** можна не ставити, бо README у тебе вже готовий окремо

6. Створи репозиторій

7. Завантаж у нього файли:
- `main.py`
- `i2c_lcd.py`
- `lcd_api.py`
- `README.md`

---

## Готовий короткий опис репозиторію

**ESP32 Wi‑Fi control panel with LCD 1602 I2C display, LED, buzzer, multilingual web interface, and light/dark theme support.**

---

## Що можна додати пізніше

- керування реле
- кнопки на корпусі
- датчик температури / вологості
- AP mode якщо немає Wi‑Fi
- OTA update
- пароль на вебпанель
- керування кількома виходами

---

## Автор

**Brain From Ukraine / BFU Electronics**

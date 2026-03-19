import network
import socket
import time
from machine import Pin, I2C
from i2c_lcd import I2cLcd

# =========================
# WIFI
# =========================
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'

# =========================
# HARDWARE
# =========================
led = Pin(2, Pin.OUT)
led.value(0)

buzzer = Pin(27, Pin.OUT)
buzzer.value(0)

# =========================
# LCD 1602 I2C
# SDA -> GPIO21
# SCL -> GPIO22
# =========================
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

devices = i2c.scan()
print("I2C devices:", devices)

lcd_addr = None
for addr in devices:
    if addr in (0x27, 0x3F):
        lcd_addr = addr
        break

if lcd_addr is None:
    raise Exception("LCD not found. Check SDA / SCL / VCC / GND")

lcd = I2cLcd(i2c, lcd_addr, 2, 16)

# current language for web page
current_lang = "en"

# current theme for web page
current_theme = "light"

# =========================
# HELPERS
# =========================
def fit16(text):
    text = str(text)
    if len(text) < 16:
        return text + (" " * (16 - len(text)))
    return text[:16]

def lcd_show(line1="", line2=""):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(fit16(line1))
    lcd.move_to(0, 1)
    lcd.putstr(fit16(line2))

def beep(ms=35):
    buzzer.value(1)
    time.sleep_ms(ms)
    buzzer.value(0)

def click():
    beep(18)

def short_beep():
    beep(45)

def long_beep():
    beep(120)

def double_click():
    click()
    time.sleep_ms(35)
    click()

def triple_click():
    click()
    time.sleep_ms(30)
    click()
    time.sleep_ms(30)
    click()

def flash_led(ms=40):
    led.value(1)
    time.sleep_ms(ms)
    led.value(0)

def pulse_feedback(ms=25):
    led.value(1)
    buzzer.value(1)
    time.sleep_ms(ms)
    led.value(0)
    buzzer.value(0)

def boot_tick():
    click()
    flash_led(15)

def boot_pulse():
    pulse_feedback(22)

def get_led_state_text():
    return "ON" if led.value() else "OFF"

# =========================
# HACKER BOOT
# LCD ONLY ENGLISH
# =========================
def hacker_boot():
    lcd_show("BFU ELECTRONICS", "BOOT SEQUENCE")
    triple_click()
    time.sleep(0.7)

    intro_frames = [
        ("[POWER]", "VIN STABLE"),
        ("[BOOT ]", "ROM LOAD"),
        ("[CLOCK]", "240MHZ OK"),
        ("[CHECK]", "FLASH MOUNT"),
        ("[CHECK]", "RAM TEST"),
        ("[CHECK]", "STACK INIT"),
    ]

    for a, b in intro_frames:
        lcd_show(a, b)
        boot_tick()
        time.sleep(0.28)

    random_frames = [
        ("BFU ELECTRONICS", ">#%&@!$*+=-<>?"),
        ("BFU ELECTRONICS", "@@##$$%%^^&&**"),
        ("BFU ELECTRONICS", "01 10 01 10 01"),
        ("BFU ELECTRONICS", "A1:F3:9C:7E:11"),
        ("BFU ELECTRONICS", "::SCAN::PORT::"),
        ("BFU ELECTRONICS", "##SYS//KERNEL#"),
        ("BFU ELECTRONICS", ">>NODE_VERIFY>"),
        ("BFU ELECTRONICS", "<<AUTH:BFU_OK>"),
    ]

    for a, b in random_frames:
        lcd_show(a, b)
        boot_pulse()
        time.sleep(0.18)

    terminal_frames = [
        ("[I2C  ]", "BUS SCAN"),
        ("[I2C  ]", "ADDR CHECK"),
        ("[GPIO ]", "MAP PINS"),
        ("[LED  ]", "GPIO2 READY"),
        ("[BUZZ ]", "GPIO27 READY"),
        ("[LCD  ]", "1602 ONLINE"),
        ("[AUTH ]", "BFU KEY OK"),
        ("[CORE ]", "LINK ACTIVE"),
    ]

    for a, b in terminal_frames:
        lcd_show(a, b)
        boot_tick()
        time.sleep(0.24)

    encrypt_frames = [
        ("SYSTEM CORE", "ENCRYPTING..."),
        ("SYSTEM CORE", "HASH CHECK..."),
        ("SYSTEM CORE", "TOKEN MATCH..."),
        ("SYSTEM CORE", "ACCESS TREE..."),
        ("SYSTEM CORE", "SECURE BOOT..."),
    ]

    for a, b in encrypt_frames:
        lcd_show(a, b)
        short_beep()
        time.sleep(0.24)

    bar_steps = [
        "[=             ]",
        "[==            ]",
        "[===           ]",
        "[=====         ]",
        "[=======       ]",
        "[=========     ]",
        "[===========   ]",
        "[============= ]",
        "[==============]",
    ]

    for step in bar_steps:
        lcd_show("SYSTEM LOADING", step)
        boot_tick()
        time.sleep(0.17)

    final_frames = [
        ("[AUTH]", "ACCESS GRANTED"),
        ("[NODE]", "BFU VERIFIED"),
        ("[CORE]", "SYSTEM READY"),
    ]

    for a, b in final_frames:
        lcd_show(a, b)
        double_click()
        time.sleep(0.35)

    lcd_show("BFU ELECTRONICS", "SYSTEM ONLINE")
    long_beep()
    led.value(1)
    time.sleep(0.35)
    led.value(0)
    time.sleep(0.6)

# =========================
# WIFI CONNECT
# =========================
def wifi_connect():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    lcd_show("NET BOOT", "START WIFI...")
    print("Connecting to Wi-Fi...")
    short_beep()
    time.sleep(0.25)

    wifi.connect(ssid, password)

    timeout = 18
    start = time.time()
    anim = 0

    connect_frames = [
        "CONNECT[    ]",
        "CONNECT[=   ]",
        "CONNECT[==  ]",
        "CONNECT[=== ]",
        "CONNECT[====]",
    ]

    while not wifi.isconnected():
        if time.time() - start > timeout:
            lcd_show("NET ERROR", "WIFI FAILED")
            long_beep()
            print("Wi-Fi failed")
            return wifi

        lcd_show("BFU ELECTRONICS", connect_frames[anim % len(connect_frames)])
        if anim % 2 == 0:
            click()
        anim += 1
        time.sleep(0.35)

    lcd_show("BFU ELECTRONICS", "WIFI LINK OK")
    double_click()
    print("Wi-Fi OK")
    time.sleep(0.8)

    lcd_show("NET STATUS", "IP REQUEST...")
    click()
    time.sleep(0.5)

    return wifi

# =========================
# LCD SCREENS
# LCD ONLY ENGLISH
# =========================
def show_ip_screen(ip):
    lcd_show("BFU ELECTRONICS", "IP:" + ip[:13])

def show_status_screen():
    state = get_led_state_text()
    lcd_show("SYSTEM STATUS", "LIGHT:" + state)

def show_server_screen():
    lcd_show("WEB CTRL ACTIVE", "SERVER ONLINE")

def show_led_changed():
    state = get_led_state_text()
    lcd_show("BFU ELECTRONICS", "LIGHT -> " + state)
    if state == "ON":
        double_click()
    else:
        click()
    time.sleep(0.85)

def show_lang_changed():
    if current_lang == "en":
        lcd_show("WEB LANGUAGE", "ENGLISH")
    else:
        lcd_show("WEB LANGUAGE", "UKRAINIAN")
    click()
    time.sleep(0.85)

def show_theme_changed():
    if current_theme == "light":
        lcd_show("WEB THEME", "LIGHT MODE")
    else:
        lcd_show("WEB THEME", "DARK MODE")
    click()
    time.sleep(0.85)

def show_ready_sequence(ip):
    ready_frames = [
        ("[WEB  ]", "SERVER READY"),
        ("[CTRL ]", "REMOTE ACCESS"),
        ("[LINK ]", ip[:16]),
    ]
    for a, b in ready_frames:
        lcd_show(a, b)
        click()
        time.sleep(0.5)

# =========================
# WEB TEXTS
# =========================
def get_texts(lang):
    if lang == "ua":
        return {
            "title": "BFU Electronics",
            "subtitle": "Керування ESP32",
            "ip_label": "IP адреса",
            "light_label": "Стан світла",
            "on_btn": "Увімкнути",
            "off_btn": "Вимкнути",
            "lang_label": "Мова",
            "theme_label": "Тема",
            "lang_en": "English",
            "lang_ua": "Українська",
            "theme_light": "Світла",
            "theme_dark": "Темна",
            "footer": "Wi-Fi керування світлодіодом",
            "status_on": "УВІМКНЕНО",
            "status_off": "ВИМКНЕНО",
            "hero": "BFU Control Panel",
        }
    else:
        return {
            "title": "BFU Electronics",
            "subtitle": "ESP32 Control Panel",
            "ip_label": "IP Address",
            "light_label": "Light State",
            "on_btn": "Turn ON",
            "off_btn": "Turn OFF",
            "lang_label": "Language",
            "theme_label": "Theme",
            "lang_en": "English",
            "lang_ua": "Українська",
            "theme_light": "Light",
            "theme_dark": "Dark",
            "footer": "Wi-Fi LED control",
            "status_on": "ON",
            "status_off": "OFF",
            "hero": "BFU Control Panel",
        }

# =========================
# THEME COLORS
# =========================
def get_theme(theme):
    if theme == "dark":
        return {
            "body_bg": "linear-gradient(180deg, #0f172a 0%, #111827 100%)",
            "text": "#eaf4ff",
            "muted": "#b7c7db",
            "card_bg": "rgba(17, 24, 39, 0.96)",
            "card_border": "rgba(96, 165, 250, 0.20)",
            "card_shadow": "0 12px 36px rgba(0, 0, 0, 0.35)",
            "brand_bg": "rgba(59, 130, 246, 0.18)",
            "brand_text": "#93c5fd",
            "panel_bg": "rgba(15, 23, 42, 0.72)",
            "panel_border": "rgba(255,255,255,0.06)",
            "row_border": "rgba(255,255,255,0.08)",
            "title": "#ffffff",
            "label": "#b7c7db",
            "value": "#ffffff",
            "badge_bg": "rgba(59, 130, 246, 0.18)",
            "badge_text": "#bfdbfe",
            "lang_bg": "#1e293b",
            "lang_text": "#e5eefc",
            "lang_border": "rgba(255,255,255,0.08)",
            "lang_active_bg": "rgba(59, 130, 246, 0.18)",
            "lang_active_text": "#bfdbfe",
            "lang_active_border": "rgba(96, 165, 250, 0.28)",
            "footer": "#a6b8cc",
        }
    else:
        return {
            "body_bg": "linear-gradient(180deg, #eaf6ff 0%, #dbeeff 100%)",
            "text": "#16324f",
            "muted": "#53718f",
            "card_bg": "rgba(255, 255, 255, 0.92)",
            "card_border": "rgba(59, 130, 246, 0.14)",
            "card_shadow": "0 12px 34px rgba(54, 112, 180, 0.14)",
            "brand_bg": "rgba(59, 130, 246, 0.10)",
            "brand_text": "#2563eb",
            "panel_bg": "rgba(245, 250, 255, 0.95)",
            "panel_border": "rgba(59,130,246,0.08)",
            "row_border": "rgba(22, 50, 79, 0.08)",
            "title": "#0f2740",
            "label": "#5c7895",
            "value": "#0f2740",
            "badge_bg": "rgba(59, 130, 246, 0.10)",
            "badge_text": "#1d4ed8",
            "lang_bg": "#f4f9ff",
            "lang_text": "#17324f",
            "lang_border": "rgba(59,130,246,0.10)",
            "lang_active_bg": "rgba(59, 130, 246, 0.12)",
            "lang_active_text": "#1d4ed8",
            "lang_active_border": "rgba(59,130,246,0.18)",
            "footer": "#6682a0",
        }

# =========================
# HTML PAGE
# =========================
def web_page(ip, lang, theme):
    t = get_texts(lang)
    th = get_theme(theme)
    state = t["status_on"] if led.value() else t["status_off"]

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{t["title"]}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: {th["body_bg"]};
            color: {th["text"]};
            min-height: 100vh;
        }}

        .wrap {{
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
            padding: 24px 16px 40px;
        }}

        .card {{
            background: {th["card_bg"]};
            border: 1px solid {th["card_border"]};
            border-radius: 24px;
            padding: 22px 18px;
            box-shadow: {th["card_shadow"]};
            backdrop-filter: blur(8px);
        }}

        .brand {{
            display: inline-block;
            padding: 7px 13px;
            border-radius: 999px;
            background: {th["brand_bg"]};
            color: {th["brand_text"]};
            font-size: 13px;
            font-weight: bold;
            margin-bottom: 14px;
        }}

        h1 {{
            margin: 0 0 6px;
            font-size: 30px;
            line-height: 1.15;
            color: {th["title"]};
        }}

        .subtitle {{
            margin: 0 0 20px;
            color: {th["muted"]};
            font-size: 15px;
        }}

        .panel {{
            background: {th["panel_bg"]};
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid {th["panel_border"]};
        }}

        .row {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            padding: 11px 0;
            border-bottom: 1px solid {th["row_border"]};
        }}

        .row:last-child {{
            border-bottom: none;
        }}

        .label {{
            color: {th["label"]};
            font-size: 14px;
        }}

        .value {{
            color: {th["value"]};
            font-weight: bold;
            text-align: right;
            word-break: break-word;
        }}

        .status-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: {th["badge_bg"]};
            color: {th["badge_text"]};
            font-size: 13px;
            font-weight: bold;
        }}

        .actions {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            margin-top: 16px;
        }}

        .btn {{
            display: block;
            width: 100%;
            text-decoration: none;
        }}

        button {{
            width: 100%;
            border: none;
            border-radius: 16px;
            padding: 16px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.08s ease;
        }}

        button:active {{
            transform: scale(0.98);
        }}

        .on {{
            background: linear-gradient(180deg, #34d399 0%, #10b981 100%);
            color: white;
        }}

        .off {{
            background: linear-gradient(180deg, #fb7185 0%, #f43f5e 100%);
            color: white;
        }}

        .section-title {{
            margin: 18px 0 10px;
            font-size: 13px;
            color: {th["muted"]};
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }}

        .switch-box {{
            display: flex;
            gap: 10px;
            margin-top: 8px;
        }}

        .switch-btn {{
            flex: 1;
            text-decoration: none;
        }}

        .switch-btn button {{
            background: {th["lang_bg"]};
            color: {th["lang_text"]};
            font-size: 15px;
            padding: 13px;
            border: 1px solid {th["lang_border"]};
        }}

        .switch-btn.active button {{
            background: {th["lang_active_bg"]};
            color: {th["lang_active_text"]};
            border: 1px solid {th["lang_active_border"]};
        }}

        .footer {{
            margin-top: 16px;
            text-align: center;
            color: {th["footer"]};
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="wrap">
        <div class="card">
            <div class="brand">BFU ELECTRONICS</div>
            <h1>{t["hero"]}</h1>
            <p class="subtitle">{t["subtitle"]}</p>

            <div class="panel">
                <div class="row">
                    <div class="label">{t["ip_label"]}</div>
                    <div class="value">{ip}</div>
                </div>
                <div class="row">
                    <div class="label">{t["light_label"]}</div>
                    <div class="value"><span class="status-badge">{state}</span></div>
                </div>
            </div>

            <div class="actions">
                <a class="btn" href="/on"><button class="on">{t["on_btn"]}</button></a>
                <a class="btn" href="/off"><button class="off">{t["off_btn"]}</button></a>
            </div>

            <div class="section-title">{t["lang_label"]}</div>
            <div class="switch-box">
                <a class="switch-btn {'active' if lang == 'en' else ''}" href="/lang/en">
                    <button>{t["lang_en"]}</button>
                </a>
                <a class="switch-btn {'active' if lang == 'ua' else ''}" href="/lang/ua">
                    <button>{t["lang_ua"]}</button>
                </a>
            </div>

            <div class="section-title">{t["theme_label"]}</div>
            <div class="switch-box">
                <a class="switch-btn {'active' if theme == 'light' else ''}" href="/theme/light">
                    <button>{t["theme_light"]}</button>
                </a>
                <a class="switch-btn {'active' if theme == 'dark' else ''}" href="/theme/dark">
                    <button>{t["theme_dark"]}</button>
                </a>
            </div>

            <div class="footer">{t["footer"]}</div>
        </div>
    </div>
</body>
</html>"""
    return html

# =========================
# START
# =========================
hacker_boot()
wifi = wifi_connect()

if not wifi.isconnected():
    raise Exception("Failed to connect to Wi-Fi")

ip = wifi.ifconfig()[0]
print("IP:", ip)

lcd_show("IP ADDRESS", ip[:16])
short_beep()
time.sleep(1.2)

# =========================
# SOCKET SERVER
# =========================
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
s.settimeout(0.2)

print("Server started:", ip)

show_ready_sequence(ip)
show_ip_screen(ip)

last_lcd_switch = time.time()
screen_mode = 0  # 0=IP, 1=STATUS, 2=SERVER

# =========================
# MAIN LOOP
# =========================
while True:
    if time.time() - last_lcd_switch > 3:
        screen_mode = (screen_mode + 1) % 3
        last_lcd_switch = time.time()

        if screen_mode == 0:
            show_ip_screen(ip)
        elif screen_mode == 1:
            show_status_screen()
        else:
            show_server_screen()

    try:
        cl, client_addr = s.accept()
    except:
        continue

    try:
        request = cl.recv(1024)
        request = str(request)
        print("Request:", request)

        if '/lang/en' in request:
            current_lang = "en"
            show_lang_changed()

        elif '/lang/ua' in request:
            current_lang = "ua"
            show_lang_changed()

        elif '/theme/light' in request:
            current_theme = "light"
            show_theme_changed()

        elif '/theme/dark' in request:
            current_theme = "dark"
            show_theme_changed()

        elif '/on' in request:
            led.value(1)
            show_led_changed()

        elif '/off' in request:
            led.value(0)
            show_led_changed()

        response = web_page(ip, current_lang, current_theme)

        cl.send('HTTP/1.1 200 OK\r\n')
        cl.send('Content-Type: text/html; charset=utf-8\r\n')
        cl.send('Connection: close\r\n\r\n')
        cl.sendall(response)
        cl.close()

    except Exception as e:
        print("Error:", e)
        try:
            cl.close()
        except:
            pass
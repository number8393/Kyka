import yfinance as yf
import requests
import time
from datetime import datetime

# Telegram настройки
TG_TOKEN = "8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs"
TG_CHAT_ID = "5556108366"

# Валютные пары (tickers на Yahoo Finance)
PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X"
}

def send_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Ошибка при отправке сообщения:", e)

def analyze_and_send():
    for name, ticker in PAIRS.items():
        try:
            data = yf.download(ticker, period="1d", interval="5m")
            if data.empty:
                send_message(f"❌ Ошибка данных: {name}")
                continue

            last = data.iloc[-1]
            close_price = last['Close']
            open_price = last['Open']

            signal = ""
            confidence = 0

            if close_price > open_price:
                signal = "📈 Покупка"
                confidence = round((close_price - open_price) / open_price * 100, 2)
            elif close_price < open_price:
                signal = "📉 Продажа"
                confidence = round((open_price - close_price) / open_price * 100, 2)
            else:
                signal = "⏸ Нет сигнала"
                confidence = 0

            if confidence > 0.1:
                send_message(
                    f"🔔 {name}\n"
                    f"{signal}\n"
                    f"Цена: {close_price:.5f}\n"
                    f"Уверенность: {confidence}%\n"
                    f"Время: {datetime.now().strftime('%H:%M:%S')}"
                )

        except Exception as e:
            send_message(f"❌ Ошибка {name}: {e}")

# Цикл проверки каждые 30 секунд
while True:
    analyze_and_send()
    time.sleep(30)

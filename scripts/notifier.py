import requests

class Notifier:
    def __init__(self, telegram_token='7763910278:AAFqZoJsJbo0wVnIYN-INR-jC5WO9WhBiXk', telegram_chat_id='5817560823'):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def send_telegram(self, message):
        if not self.telegram_token or not self.telegram_chat_id:
            print("Telegram token or chat_id not set.")
            return
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {"chat_id": self.telegram_chat_id, "text": message}
        requests.post(url, data=data)

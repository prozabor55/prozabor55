import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из .env

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    """Отправляет сообщение в личный чат с ботом."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("TELEGRAM_TOKEN или TELEGRAM_CHAT_ID не заданы!")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()

    if not name or not phone:
        return jsonify({'success': False, 'message': 'Имя и телефон обязательны'}), 400

    message = (
        f"🆕 <b>Новая заявка с сайта ПроЗабор55</b>\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}"
    )

    if send_telegram_message(message):
        return jsonify({'success': True, 'message': 'Заявка отправлена! Мы скоро свяжемся с вами.'})
    else:
        return jsonify({'success': False, 'message': 'Ошибка отправки. Пожалуйста, позвоните нам.'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
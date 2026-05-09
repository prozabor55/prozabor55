import os
import vk_api
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из .env

app = Flask(__name__)

# Настройки VK
VK_ACCESS_TOKEN = os.environ.get('VK_ACCESS_TOKEN')  # Ключ доступа сообщества
VK_USER_ID = os.environ.get('VK_USER_ID')  # Ваш ID пользователя (кто получит уведомление)

def send_vk_message(text):
    """Отправляет сообщение в VK (личное сообщение пользователю)."""
    if not VK_ACCESS_TOKEN or not VK_USER_ID:
        print("VK_ACCESS_TOKEN или VK_USER_ID не заданы!")
        return False
    
    try:
        # Авторизация через токен сообщества
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        vk = vk_session.get_api()
        
        # Отправка сообщения
        vk.messages.send(
            user_id=int(VK_USER_ID),  # ID получателя (администратора)
            message=text,
            random_id=0  # обязательный параметр для VK API
        )
        print("Сообщение в VK успешно отправлено")
        return True
        
    except Exception as e:
        print(f"Ошибка отправки в VK: {e}")
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
        f"🆕 Новая заявка с сайта ПроЗабор55\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}"
    )

    if send_vk_message(message):
        return jsonify({'success': True, 'message': 'Заявка отправлена! Мы скоро свяжемся с вами.'})
    else:
        return jsonify({'success': False, 'message': 'Ошибка отправки. Пожалуйста, позвоните нам.'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
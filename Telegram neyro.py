import telebot
import requests
import re
import os
import time

"""Получает готовый ответ от API"""
def fetch_fresh_message(response_message_id):
    url = 'https://yandex.ru/neuralsearch/api/get_fresh_message?lr='
    data = {"ResponseMessageId": response_message_id}
    
    while True:
        response = requests.post(
            url,
            headers={'cookie': f'Session_id={os.getenv("YANDEXRU_SESSIONID_COOK")}'},
            json=data
        )
        
        result = response.json()
        #print("Статус запроса:", result)  # Вывод сырого ответа
        
        if result.get('IsCompleteResults'):
            # Очистка ответа от маркдаун-ссылок
            clean_text = re.sub(r'\[\`\`\`\d+\`\`\`\]\(.*?\)', '', result.get('TargetMarkdownText', ''))
            return clean_text
            
        time.sleep(result.get('RetryRecommendationMs', 1000) / 1000)
"""Отправляет запрос в нейросеть"""
def send_request(user_request):
    url = 'https://yandex.ru/neuralsearch/api/send_to_dialog?lr='
    data = {"UserRequest": user_request}

    
    response = requests.post(
        url,
        headers={'cookie': f'Session_id={os.getenv("YANDEXRU_SESSIONID_COOK")}'},
        json=data
    )
    
    response_data = response.json()
    #print("Первоначальный ответ API:", response_data)  # Вывод сырого ответа
    
    response_message_id = response_data['ResponseMessageId']

    
    
    return fetch_fresh_message(response_message_id)
    


bot = telebot.TeleBot("token", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, f"👋Привет {message.from_user.first_name}! \n🤖Этот бот создан для общения с яндекс нейро без яндекса. \n📝Введите запрос, чтобы начать.")
	

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    mes = bot.send_message(message.chat.id, f"Ожидание яндекс нейро (≈ 5 секунд)🔄...")

    result = send_request(message.text)

    finalresult = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result)
    

    bot.delete_message(message.chat.id, mes.message_id)

    bot.send_message(message.chat.id, finalresult, parse_mode="HTML")

	
	
	
	

bot.infinity_polling()
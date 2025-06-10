import requests
import re
import os
import time

def fetch_fresh_message(response_message_id):
    """Получает готовый ответ от API"""
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

def send_request(user_request):
    """Отправляет запрос в нейросеть"""
    url = 'https://yandex.ru/neuralsearch/api/send_to_dialog?lr='
    data = {"UserRequest": user_request}

    try:
        response = requests.post(
            url,
            headers={'cookie': f'Session_id={os.getenv("YANDEXRU_SESSIONID_COOK")}'},
            json=data
        )
        
        response_data = response.json()
        #print("Первоначальный ответ API:", response_data)  # Вывод сырого ответа
        
        submissions_left = response_data['ResponseStatus']['LimitsInfo']['SubmissionsLeft']
        CommentByLang = response_data['ResponseStatus']['LimitsInfo']["CommentByLang"]["ru"]
        print(CommentByLang)
        response_message_id = response_data['ResponseMessageId']

        if submissions_left == 0:
            print("Лимит запросов исчерпан")
            return "Количество запросов в час ограничено."
        
        return fetch_fresh_message(response_message_id)
    except Exception as e:
        print("Ошибка при обработке запроса:", e)
        return "Произошла ошибка, попробуйте позднее"

def main():
    """Основная функция для тестирования"""
    print("Введите ваш запрос:")
    user_input = input().strip()
    
    if user_input:
        print("\nОтправка запроса...")
        result = send_request(user_input)
        print("\nОтвет от нейросети:")
        print(result)
    else:
        print("Запрос не может быть пустым")

if __name__ == "__main__":
    main()
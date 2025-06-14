import requests
import re


user_input = input("Введите ваш запрос: ").strip()
print("\nОтправка запроса...")
if user_input:
    response = requests.post("https://yandex.ru/neuralsearch/api/send_to_dialog?lr=", headers={'cookie': f'Session_id=None'}, json={"UserRequest": user_input})
    
    response_data = response.json()

    CommentByLang = response_data['ResponseStatus']['LimitsInfo']["CommentByLang"]["ru"]
    print(f"\n{CommentByLang}")

    response_message_id = response_data['ResponseMessageId']

    while True:
        response = requests.post("https://yandex.ru/neuralsearch/api/get_fresh_message?lr=", headers={'cookie': f'Session_id=None'}, json={"ResponseMessageId": response_message_id})
        
        result = response.json()
        
        if result["IsCompleteResults"]:
            break
            

    text = re.sub(r'\[\`\`\`\d+\`\`\`\]\([^)]+\)', '', result["TargetMarkdownText"])
    text = re.sub(r'\*\*', '', text)
    print(text)
   
else:
    print("Запрос не может быть пустым")


import requests
import json
import warnings
warnings.filterwarnings("ignore")

class GigaChat:
    def __init__(self, auth_key: str, client_id: str, scope: str):
        self.client_id = client_id
        self.scope = scope
        self.access_token = self.auth(auth_key)

    def auth(self, auth_key: str) -> str:
        url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
        headers = {
            'RqUID': '6f0b1291-c7f3-43c6-bb2e-9f3efb2dc98e',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + auth_key,
        }
        data = {'scope': self.scope}

        response = requests.post(url, headers=headers, data=data, verify=False)
        if response.status_code != 200:
            raise Exception('Не могу получить access_token')

        response_json = json.loads(response.text)
        return response_json['access_token']

    def get_recipe(self, dish_name: str) -> dict:
        url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'X-Request-ID': '79e41a5f-f180-4c7a-b2d9-393086ae20a1',
            'X-Session-ID': 'b6874da0-bf06-410b-a150-fd5f9164a0b2',
            'X-Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }
        data = {
            "model": "GigaChat",
            "stream": False,
            "update_interval": 0,
            "messages": [
                {
                    "role": "system",
                    "content":
                        f'Сгенерируй рецепт блюда "{dish_name}".' +
                        "Следуй следующим требованиям: используемые объекты и их названия должны быть уникальными," +
                        "не создавай несуществующих терминов или фраз. Если закончились варианты или введённый запрос " +
                        "не является названием блюда, верни пустую строку." +
                        "Верни результат в формате JSON-массива, без дополнительных пояснений. Пример формата:" +
                        "{" +
                        "\"title\": \"название объекта\"," +
                        "\"description\": \"описание объекта\"," +
                        "\"ingredients\": [{\"name\": \"название ингредиента\", \"amount\": \"количество в граммах\"}]," +
                        "\"instruction\": \"инструкция по приготовлению\"" +
                        "}."
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code != 200:
            raise Exception(f'Не могу получить блюдо {dish_name} от GigaChat')

        response_json = json.loads(response.text)
        dish_str = response_json['choices'][0]['message']['content']
        if dish_str == "":
            raise Exception(f'Не могу обработать {dish_name}, потому что это не блюдо')

        dish_json = json.loads(dish_str)
        return {
            'title': dish_json['title'],
            'description': dish_json['description'],
            'ingredients': dish_json['ingredients'],
            'instruction': dish_json['instruction']
        }

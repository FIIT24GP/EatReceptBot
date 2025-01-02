import requests
import json

class SberMarket:
    def __init__(self, region_id: int, place_slug: str, location: dict):
        """
        Инициализация объекта для работы с API Яндекс Еда.

        :param region_id: Идентификатор региона.
        :param place_slug: Идентификатор магазина/ресторана.
        :param location: Координаты {lat: широта, lon: долгота}.
        """
        self.region_id = region_id
        self.place_slug = place_slug
        self.location = location

    def get_product(self, product_name: str) -> dict:
        """
        Поиск продукта по названию.

        :param product_name: Название продукта.
        :return: Словарь с URL и ценой продукта.
        """
        url = 'https://eda.yandex.ru/api/v1/menu/search'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru',
            'content-type': 'application/json;charset=UTF-8'
        }
        data = {
            "region_id": self.region_id,
            "place_slug": self.place_slug,
            "text": product_name,
            "location": self.location
        }
        response = requests.post(url, headers=headers, json=data, verify=False)

        if response.status_code != 200:
            raise Exception(f'Не удалось получить информацию по продукту: {product_name}')

        response_json = response.json()
        products = response_json.get('blocks', [])[0].get('payload', {}).get('products', [])

        if not products:
            return {'url': '', 'price': ''}

        product = products[0]
        return {
            'url': f'https://eda.yandex.ru/retail/{self.place_slug}?item={product["public_id"]}',
            'price': product.get('price', 'Не указана')
        }

    def get_ready_meals(self, meal_name: str) -> list:
        """
        Поиск готовых блюд по названию.

        :param meal_name: Название блюда.
        :return: Список готовых блюд с ценами, описанием и ссылками.
        """
        url = 'https://eda.yandex.ru/api/v1/menu/search'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8'
        }
        data = {
            "region_id": self.region_id,
            "place_slug": self.place_slug,
            "text": meal_name,
            "location": self.location
        }
        response = requests.post(url, headers=headers, json=data, verify=False)

        if response.status_code != 200:
            raise Exception(f'Не удалось найти готовые блюда по запросу: {meal_name}')

        response_json = response.json()
        ready_meals = response_json.get('blocks', [])[0].get('payload', {}).get('products', [])

        result = []
        for meal in ready_meals:
            result.append({
                "name": meal.get("name"),
                "price": meal.get("price", "Не указана"),
                "description": meal.get("description", "Описание отсутствует"),
                "url": f'https://eda.yandex.ru/retail/{self.place_slug}?item={meal["public_id"]}'
            })

        return result

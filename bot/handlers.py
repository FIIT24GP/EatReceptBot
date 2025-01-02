from bot.gigachat_service import GigaChat
from bot.yandex_service import SberMarket
from config import *

# Инициализация GigaChat
gigaChat = GigaChat(
    auth_key=auth_key,
    client_id=client_id,
    scope='GIGACHAT_API_PERS'
)

# Инициализация SberMarket
sberMarket = SberMarket(
    region_id=1,
    place_slug="perekrestok",
    location={
        "lat": 55.739727,
        "lon": 37.408067
    }
)

def process_dish(dish_name: str):
    """
    Обрабатывает запрос пользователя: получает рецепт из GigaChat и информацию о готовых блюдах.
    """
    try:
        # Получение рецепта из GigaChat
        dish = gigaChat.get_recipe(dish_name)
        ingredients_info = []

        # Формируем список ингредиентов с ссылками на покупку
        for ingredient in dish['ingredients']:
            ingredient_name = ingredient['name']
            ingredient_amount = ingredient['amount']

            # Поиск продукта через SberMarket
            sbermarket_product = sberMarket.get_product(ingredient_name)
            product_url = sbermarket_product.get('url', 'Ссылка не найдена')

            ingredients_info.append(f"{ingredient_name} ({ingredient_amount}): {product_url}")

        # Получение готовых блюд
        ready_meals = sberMarket.get_ready_meals(dish_name)
        if ready_meals:
            ready_meals_info = "\n\n".join([
                f"Название: {meal['name']}\n"
                f"Цена: {meal['price']} руб\n"
                f"Описание: {meal['description']}\n"
                f"Ссылка: {meal['url']}"
                for meal in ready_meals
            ])
        else:
            ready_meals_info = "Готовые блюда не найдены."

        # Формирование итогового ответа
        response = (
            f"Название: {dish['title']}\n\n"
            f"Описание: {dish['description']}\n\n"
            f"Ингредиенты:\n" + "\n".join(ingredients_info) + "\n\n"
            f"Инструкция:\n{dish['instruction']}\n\n"
            f"Готовое блюдо:\n{ready_meals_info}"
        )

        return response

    except KeyError as e:
        return f"Ошибка обработки данных: отсутствует ключ {str(e)}."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

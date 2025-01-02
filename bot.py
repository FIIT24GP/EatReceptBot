import asyncio
from bot.handlers import process_dish as process_dish_request  # Исправлено имя функции
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
import config

# Создание объектов бота, диспетчера и маршрутизатора
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
router = Router()

# Регистрация хендлеров
@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer("Добро пожаловать! Напишите название блюда, чтобы получить рецепт и информацию о готовых блюдах.")

@router.message()
async def recipe_handler(message: Message):
    try:
        # Обработка запроса на рецепт
        response = process_dish_request(message.text)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


# Основная функция для запуска бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)  # Удалить старые вебхуки
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот запускается!")
    asyncio.run(main())

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Привет! Я Quiz Bot. Введи /quiz чтобы начать!")

# Простой запуск теста
@dp.message(F.text == "/quiz")
async def quiz(message: Message):
    await message.answer("Вопрос 1: Как называется столица Франции?\nОтвет: ...")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    dp.run_polling(bot)
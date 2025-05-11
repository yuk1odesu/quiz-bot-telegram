from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
import os
from dotenv import load_dotenv

# Загрузка токена из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База вопросов
questions = [
    {
        "question": "Какая столица Франции?",
        "options": ["Париж", "Лондон", "Берлин"],
        "correct": "Париж",
    },
    {
        "question": "Сколько цветов в радуге?",
        "options": ["5", "7", "6"],
        "correct": "7",
    },
    {
        "question": "Как называется столица Японии?",
        "options": ["Пекин", "Токио", "Сеул"],
        "correct": "Токио",
    },
]

# Глобальные переменные для хранения состояния
current_question_index = 0
score = 0


# Команда /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Я Quiz Bot. Напиши /quiz чтобы начать викторину!")


# Команда /quiz
@dp.message(Command(commands=["quiz"]))
async def cmd_quiz(message: Message):
    global current_question_index, score
    current_question_index = 0
    score = 0
    await send_question(message)


# Отправка текущего вопроса
async def send_question(message: Message):
    question_data = questions[current_question_index]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=option, callback_data=f"answer_{option}")]
            for option in question_data["options"]
        ]
    )
    await message.answer(question_data["question"], reply_markup=keyboard)


# Обработка ответа
@dp.callback_query(F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery):
    global current_question_index, score

    user_answer = callback.data.replace("answer_", "")
    correct_answer = questions[current_question_index]["correct"]

    if user_answer == correct_answer:
        await callback.message.answer("✅ Правильно!")
        score += 1
    else:
        await callback.message.answer(f"❌ Неправильно. Правильный ответ: {correct_answer}")

    current_question_index += 1

    if current_question_index < len(questions):
        await send_question(callback.message)
    else:
        await callback.message.answer(f"🏁 Викторина окончена!\nТвой результат: {score} из {len(questions)}")
        await callback.message.answer("Напиши /quiz чтобы попробовать снова.")


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    dp.run_polling(bot)
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

TOKEN = '7283062231:AAHKpYPqzP90H8c1VHiGzRpWe3d-9dQJ860'

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сантиметры в дюймы"), KeyboardButton(text="Дюймы в сантиметры")],
        [KeyboardButton(text="Метры в ярды"), KeyboardButton(text="Ярды в метры")],
        [KeyboardButton(text="Километры в мили"), KeyboardButton(text="Мили в километры")],
        [KeyboardButton(text="/help"), KeyboardButton(text="/about")]
    ],
    resize_keyboard=True
)

# Состояния
class ConversionState(StatesGroup):
    waiting_for_value = State()
    conversion_type = State()

# Функции конвертации
def cm_to_inches(cm):
    return cm / 2.54

def inches_to_cm(inches):
    return inches * 2.54

def meters_to_yards(meters):
    return meters * 1.09361

def yards_to_meters(yards):
    return yards / 1.09361

def km_to_miles(km):
    return km / 1.60934

def miles_to_km(miles):
    return miles * 1.60934

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Добро пожаловать в бот-конвектор длин. Выберите единицы измерения с помощью клавиатуры.", reply_markup=keyboard)

@dp.message(Command("help"))
async def send_help(message: Message):
    help_text = (
        "Доступные команды и преобразования:\n"
        "/start - Старт бота\n"
        "/help - Помощь\n"
        "/about - Узнай больше об этом боте\n"
        "Сантиметры в дюймы - Переводит сантиметры в дюймы\n"
        "Дюймы в сантиметры - Переводит дюймы в сантиметры\n"
        "Метры в ярды - Переводит метры в ярды\n"
        "Ярды в метры - Переводит ярды в метры\n"
        "Километры в мили - Переводит километры в мили\n"
        "Мили в километры - Переводит мили в километры\n"
    )
    await message.answer(help_text, reply_markup=keyboard)

@dp.message(Command("about"))
async def send_about(message: Message):
    about_text = "Этот бот может переводить указанную длину из Международной системы измерения (СИ) в Английскую систему измерения."
    await message.answer(about_text, reply_markup=keyboard)

@dp.message(lambda message: message.text in ["Сантиметры в дюймы", "Дюймы в сантиметры", "Метры в ярды", "Ярды в метры", "Километры в мили", "Мили в километры"])
async def handle_conversion(message: Message, state: FSMContext):
    await state.update_data(conversion_type=message.text)
    await state.set_state(ConversionState.waiting_for_value)
    if message.text == "Сантиметры в дюймы":
        await message.answer("Введите сантиметры:")
    elif message.text == "Дюймы в сантиметры":
        await message.answer("Введите дюймы:")
    elif message.text == "Метры в ярды":
        await message.answer("Введите метры:")
    elif message.text == "Ярды в метры":
        await message.answer("Введите ярды:")
    elif message.text == "Километры в мили":
        await message.answer("Введите километры:")
    elif message.text == "Мили в километры":
        await message.answer("Введите мили:")

@dp.message(ConversionState.waiting_for_value)
async def handle_conversion_input(message: Message, state: FSMContext):
    try:
        value = float(message.text)
        data = await state.get_data()
        conversion_type = data['conversion_type']
        if conversion_type == "Сантиметры в дюймы":
            result = cm_to_inches(value)
            await message.answer(f"{value} сантиметров =  {result:.2f} дюймов.", reply_markup=keyboard)
        elif conversion_type == "Дюймы в сантиметры":
            result = inches_to_cm(value)
            await message.answer(f"{value} дюймов = {result:.2f} сантиметров.", reply_markup=keyboard)
        elif conversion_type == "Метры в ярды":
            result = meters_to_yards(value)
            await message.answer(f"{value} метров = {result:.2f} ярдов.", reply_markup=keyboard)
        elif conversion_type == "Ярды в метры":
            result = yards_to_meters(value)
            await message.answer(f"{value} ярдов = {result:.2f} метров.", reply_markup=keyboard)
        elif conversion_type == "Километры в мили":
            result = km_to_miles(value)
            await message.answer(f"{value} километров = {result:.2f} миль.", reply_markup=keyboard)
        elif conversion_type == "Мили в километры":
            result = miles_to_km(value)
            await message.answer(f"{value} миль = {result:.2f} километров.", reply_markup=keyboard)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.", reply_markup=keyboard)
    finally:
        await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
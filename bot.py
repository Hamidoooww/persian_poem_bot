import sqlite3
import asyncio
from turtle import st
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import Bot , Dispatcher, F, types
from aiogram.filters import Command
import database
import os


TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('poems.db')
cursor = conn.cursor()

current_poet_name = ""
current_book_name = ""
current_part_name = ""
class PoemStates(StatesGroup):
    waiting_for_book = State()
    waiting_for_part = State()
    waiting_for_poem = State()

@dp.message(Command("start"))
async def start_butten(message : types.Message):
    await message.answer("سلام به بان شعر فاری خوشومدی \n یکی از گزینه های زیر رو انتخاب کن",
                          reply_markup=types.ReplyKeyboardMarkup(keyboard=[
                              [types.KeyboardButton(text="شعر رندوم")],
                              [types.KeyboardButton(text="اشعار سعدی")],
                              [types.KeyboardButton(text="ارتباط با ادمین")]
                          ],resize_keyboard=True))


@dp.message(F.text == "شعر رندوم")
async def send_random_poem(message: types.Message):
    message_text = database.get_random_poem()
    if message_text:
        await message.answer(message_text, parse_mode="Markdown")
    else:
        await message.answer("متاسفانه هیچ شعری پیدا نشد\n لطفا دوباره تلاش کنید")

@dp.message(F.text == "اشعار سعدی")
async def send_saadi_poems(message: types.Message):
    books = database.get_books_by_poet("سعدی")
    keyboard_bottons = []
    for book in books:
        keyboard_bottons.append([types.KeyboardButton(text=book[0])])
    keyboard_bottons.append([types.KeyboardButton(text="بازگشت به منوی اصلی")])
    await message.answer("لطفا یکی از کتاب های شاعر را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))
    await State.set_state(PoemStates.waiting_for_book)
    current_poet_name = "سعدی"

@dp.message(PoemStates.waiting_for_book)
async def send_parts(message: types.Message, state: FSMContext):
    if message.text == "بازگشت به منوی اصلی":
        await state.clear()
        await start_butten(message)

    elif message.text not in [book[0] for book in database.get_books_by_poet("سعدی")]:
        await message.answer("لطفا یکی از کتاب های شاعر را انتخاب کنید")
    else:
        parts = database.get_parts_by_book(message.text)
        keyboard_bottons = []
        for part in parts:
            keyboard_bottons.append([types.KeyboardButton(text=part[0])])
        keyboard_bottons.append([types.KeyboardButton(text="بازگشت به شاعر")])
        await message.answer("لطفا یکی از پارت های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))
        await State.set_state(PoemStates.waiting_for_part)
        current_book_name = message.text

@dp.message(PoemStates.waiting_for_part)
async def send_parts(message: types.Message, state: FSMContext):
    if message.text == "بازگشت به شاعر":
        await state.set_state(PoemStates.waiting_for_book)
        await send_saadi_poems(message)
    elif message.text not in [part[0] for part in database.get_parts_by_book(message.text)]:
        await message.answer("لطفا یکی از پارت های کتاب را انتخاب کنید")
    else:
        poems_number = database.get_poem_count_by_part(message.text, message.text)
        await message.answer(f"تعداد شعر های این پارت {poems_number} می باشد\n لطفا عدد شعر مورد نظر خود را وارد کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=[
            [types.KeyboardButton(text="بازگشت به انتخاب پارت")],
        ], resize_keyboard=True))
        current_part_name = message.text

@dp.message(PoemStates.waiting_for_poem)
async def send_poem(message: types.Message, state: FSMContext):
    if message.text == "بازگشت به انتخاب پارت":
        await state.set_state(PoemStates.waiting_for_part)
        await send_parts(message, state)
    else:
        try:
            poem_number = int(message.text)
            part_name = current_part_name
            book_name = current_book_name
            poem_text = database.get_poem_text_by_number(part_name, book_name, poem_number)
            if poem_text:
                await message.answer(f'{poem_text[0]}\n\n```{poem_text[2]}\n{poem_text[1]}\n```', parse_mode="Markdown")
            else:
                await message.answer("شعر مورد نظر پیدا نشد\n لطفا دوباره تلاش کنید")
        except ValueError:
            await message.answer("لطفا یک عدد معتبر وارد کنید")
        


@dp.message(F.text == "ارتباط با ادمین")
async def contact_admin(message: types.Message):
    await message.answer("برای ارتباط با ادمین لطفا به آیدی زیر پیام دهید\n\n@Hamidoooww")

async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())

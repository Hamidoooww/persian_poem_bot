import sqlite3
import asyncio
from aiogram.types import inline_keyboard_button    
from aiogram import Bot , Dispatcher, F, types
from aiogram.filters import Command
import database
import os


TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('poems.db')
cursor = conn.cursor()

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
    cursor.execute("SELECT book_name FROM books WHERE poets_id = '1'")
    books = cursor.fetchall()
    if books:
        keyboard = types.ReplyKeyboardMarkup(keyboard=[
            *[[types.KeyboardButton(text=book[0])] for book in books],
                [types.KeyboardButton(text='بازگشت')
                ]
                ],
              resize_keyboard=True)
        await message.answer("لطفا یکی از کتاب های شاعر را انتخاب کنید",reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())
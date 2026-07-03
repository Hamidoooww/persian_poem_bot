import sqlite3
import asyncio
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
        keyboard_bottons.append([types.KeyboardButton(text=book)])
    await message.answer("لطفا یکی از کتاب های شاعر را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))


@dp.message(F.text == "بوستان")
async def send_booston_poems(message: types.Message):
    parts = database.get_parts_by_book("بوستان")
    keyboard_bottons = []
    for part in parts:
        keyboard_bottons.append([types.KeyboardButton(text=part)])
    await message.answer("لطفا یکی از بخش های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))



@dp.message(F.text == "خبیثات و مجالس الهزل")
async def send_khobithat_poems(message: types.Message):
    parts = database.get_parts_by_book("خبیثات و مجالس الهزل")
    keyboard_bottons = []
    for part in parts:
        keyboard_bottons.append([types.KeyboardButton(text=part)])
    await message.answer("لطفا یکی از بخش های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))

@dp.message(F.text == "دیوان اشعار")
async def send_divan_poems(message: types.Message):
    parts = database.get_parts_by_book("دیوان اشعار")
    keyboard_bottons = []
    for part in parts:
        keyboard_bottons.append([types.KeyboardButton(text=part)])
    await message.answer("لطفا یکی از بخش های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))

@dp.message(F.text == "مواعظ")
async def send_mavaaez_poems(message: types.Message):
    parts = database.get_parts_by_book("مواعظ")
    keyboard_bottons = []
    for part in parts:
        keyboard_bottons.append([types.KeyboardButton(text=part)])
    await message.answer("لطفا یکی از بخش های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))

@dp.message(F.text == "گلستان")
async def send_golestaan_poems(message: types.Message):
    parts = database.get_parts_by_book("گلستان")
    keyboard_bottons = []
    for part in parts:
        keyboard_bottons.append([types.KeyboardButton(text=part)])
    await message.answer("لطفا یکی از بخش های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_bottons, resize_keyboard=True))

@dp.message(F.text == "ارتباط با ادمین")
async def contact_admin(message: types.Message):
    await message.answer("برای ارتباط با ادمین لطفا به آیدی زیر پیام دهید\n\n@Hamidoooww")

async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())

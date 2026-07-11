import sqlite3
import asyncio
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import database

# حتما توکن جدید رو جایگزین کن و به صورت متغیر محیطی (env) بگیر
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

class PoemStates(StatesGroup):
    waiting_for_book = State()
    waiting_for_part = State()
    waiting_for_poem = State()

@dp.message(Command("start"))
async def start_button(message: types.Message, state: FSMContext):
    await state.clear() # همیشه در استارت استیت رو پاک کن تا ربات هنگ نکنه
    await message.answer("سلام به بات شعر فارسی خوش‌اومدی \n یکی از گزینه‌های زیر رو انتخاب کن",
                          reply_markup=types.ReplyKeyboardMarkup(keyboard=[
                              [types.KeyboardButton(text="شعر رندوم")],
                              [types.KeyboardButton(text="آثار شاعران")],
                              [types.KeyboardButton(text="ارتباط با ادمین")]
                          ], resize_keyboard=True))

@dp.message(F.text == "شعر رندوم")
async def send_random_poem(message: types.Message):
    try:
        message_text = database.get_random_poem()
        if message_text:
            await message.answer(message_text, parse_mode="Markdown")
        else:
            await message.answer("متاسفانه هیچ شعری پیدا نشد\n لطفا دوباره تلاش کنید")
    except Exception as e:
        print(e)

@dp.message(F.text == "آثار شاعران")
async def send_poets_name(message: types.Message):
    try:
        poets = database.get_poets()
        glass_key = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text="سعدی", callback_data="sadi")],[InlineKeyboardButton(text='بازگشت به منوی اصلی', callback_data='back_to_menu')]])
        await message.answer("لطفا یکی از شاعران زیر را انتخاب کنی  \n (با عرض پوزش فعلا فقط سعدی رو داریم)",
                              reply_markup= glass_key)
    except:
        await message.answer('بات را مجدد استارت کنید')

@dp.callback_query(F.data == "sadi")
async def send_saadi_poems(call_back : types.CallbackQuery, state : FSMContext):
    books = database.get_books_by_poet("سعدی")
    keyboard_buttons = [[types.KeyboardButton(text=book[0])] for book in books]
    keyboard_buttons.append([types.KeyboardButton(text="بازگشت به منوی اصلی")])
    
    await call_back.answer()
    await call_back.message.answer("لطفا یکی از کتاب‌های شاعر را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))
    await state.set_state(PoemStates.waiting_for_book)
    await state.update_data(current_poet_name="سعدی")

# تغییر نام به process_book_selection
@dp.message(PoemStates.waiting_for_book)
async def process_book_selection(message: types.Message, state: FSMContext):
    if message.text == "بازگشت به منوی اصلی":
        await state.clear()
        await start_button(message, state)
        
    elif message.text not in [book[0] for book in database.get_books_by_poet("سعدی")]:
        await message.answer("لطفا یکی از کتاب‌های شاعر را انتخاب کنید")
        
    else:
        parts = database.get_parts_by_book(message.text)
        keyboard_buttons = [[types.KeyboardButton(text=part[0])] for part in parts]
        keyboard_buttons.append([types.KeyboardButton(text="بازگشت به شاعر")])
        
        await message.answer("لطفا یکی از پارت‌های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))
        await state.set_state(PoemStates.waiting_for_part)
        await state.update_data(current_book_name=message.text)

# تغییر نام به process_part_selection
@dp.message(PoemStates.waiting_for_part)
async def process_part_selection(message: types.Message, state: FSMContext):
    if message.text == "بازگشت به شاعر":
        await state.set_state(PoemStates.waiting_for_book)
        await send_saadi_poems(message, state)
        return

    # خواندن صحیح دیتا با await
    user_data = await state.get_data()
    book_name = user_data.get("current_book_name")
    
    # اینجا باید book_name رو به دیتابیس پاس بدی
    valid_parts = [part[0] for part in database.get_parts_by_book(book_name)]

    if message.text in valid_parts:
        poem_count = database.get_poem_count_by_part(message.text, book_name)
        await message.answer(f"این پارت {poem_count} شعر دارد\nلطفا شماره شعر مورد نظر خود را وارد کنید", 
                             reply_markup=types.ReplyKeyboardMarkup(keyboard=[
                                 [types.KeyboardButton(text="بازگشت به انتخاب پارت")]
                             ], resize_keyboard=True))
        await state.set_state(PoemStates.waiting_for_poem)
        await state.update_data(current_part_name=message.text)
    else:
         await message.answer("لطفا یکی از پارت‌ها را از منو انتخاب کنید.")

@dp.message(PoemStates.waiting_for_poem)
async def send_poem(message: types.Message, state: FSMContext):
    if message.text == "بازگشت به انتخاب پارت":
        # برای بازگشت به پارت، باید لیست پارت‌ها رو دوباره بهش نشون بدیم
        user_data = await state.get_data()
        book_name = user_data.get("current_book_name")
        
        parts = database.get_parts_by_book(book_name)
        keyboard_buttons = [[types.KeyboardButton(text=part[0])] for part in parts]
        keyboard_buttons.append([types.KeyboardButton(text="بازگشت به شاعر")])
        
        await message.answer("لطفا یکی از پارت‌های کتاب را انتخاب کنید", reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))
        await state.set_state(PoemStates.waiting_for_part)
        return

    try:
        poem_number = int(message.text)
        
        # خواندن صحیح دیتا با await
        user_data = await state.get_data()
        part_name = user_data.get("current_part_name")
        book_name = user_data.get("current_book_name")
        
        poem_text = database.get_poem_text_by_number(part_name, book_name, poem_number)
        
        if poem_text:
            await message.answer(f'{poem_text[0]}\n\n```\n{poem_text[2]}\n{poem_text[1]}\n```', parse_mode="Markdown")
        else:
            await message.answer("شعر مورد نظر پیدا نشد\n لطفا یک عدد دیگر وارد کنید")
    except ValueError:
        await message.answer("لطفا فقط یک عدد معتبر (مثلا 12) وارد کنید")

@dp.message(F.text == "ارتباط با ادمین")
async def contact_admin(message: types.Message):
    await message.answer("برای ارتباط با ادمین لطفا به آیدی زیر پیام دهید\n\n@Hamidoooww")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
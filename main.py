import asyncio
import logging
import time
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config
from os import listdir, path

API_TOKEN = config('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class MenuState(StatesGroup):
    category = State()
    product = State()

    
def get_keyboard_from_path(sources):
    categ_keyboard = types.InlineKeyboardMarkup()
    
    if path.exists(sources):
            list_categ = listdir(sources)
               
    for dir in list_categ:
            # print(dir)
            button = types.InlineKeyboardButton(dir, callback_data=dir)
            categ_keyboard.add(button)
    
    return categ_keyboard
    
def get_data_from_json(source):
    with open(source, "r", encoding='utf_8') as f:
        data = json.load(f)
        print(data)    
    return data
    


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    state.finish()
    markup = get_keyboard_from_path('shop')
    await message.reply("Виберите категорию товара:",reply_markup=markup)
    await MenuState.category.set()

@dp.callback_query_handler(state= MenuState.category)
async def menu_category(clq: types.CallbackQuery, state: FSMContext):
    # print(clq.data)
    async with state.proxy() as data:
        data['category'] = clq.data
    
    markup = get_keyboard_from_path('shop/'+clq.data)
    await clq.message.edit_text("Виберите товара:",reply_markup=markup)
    await MenuState.product.set()
    
@dp.callback_query_handler(lambda c: c.data == 'back',state= MenuState.product)
async def menu_product_back(clq: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data['category'] 
    markup = get_keyboard_from_path('shop/'+category)
    await bot.send_message(clq.message.chat.id,"Виберите товара:",reply_markup=markup)
    await clq.message.delete()
   
@dp.callback_query_handler(state= MenuState.product)
async def menu_product(clq: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['product'] = clq.data
        source = f"shop/{data.get('category')}/{data.get('product')}/{data.get('product')}.json"
        source_img = f"shop/{data.get('category')}/{data.get('product')}/img/{data.get('product')}.png"  
        data['source'] = source
    # data = await state.get_data()
    product = get_data_from_json(source)
    text = f"<b>Назва</b>: {product.get('name')}\n"\
            f"<b>Рівень</b>: {product.get('level')}\n"\
            f"<b>Ціна</b>: {product.get('prices')}\n\n"\
            f"<b>Кількість уроків</b>: {product.get('lessons_count')}\n"\
            f"<b>Опис</b>: {product.get('description')}\n"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤔LINK",url=product.get('link')))
    markup.add(types.InlineKeyboardButton("👈BACK", callback_data='back'))
    # media = 
    photo = types.InputFile(source_img)
    await bot.send_photo(clq.message.chat.id,photo,"Інформація товару:\n"+text,reply_markup=markup, parse_mode= 'HTML')
    await clq.message.delete()
    # await clq.message.edit_text("Інформація товару:\n"+text,reply_markup=markup, parse_mode= 'HTML')



    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



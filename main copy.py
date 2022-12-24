import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config


API_TOKEN = config('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



button_hi = types.KeyboardButton('ЗАРЕГАТЬСЯ! 👋')
greet_kb = types.ReplyKeyboardMarkup()
greet_kb.add(button_hi)


g_inline_keyboard = types.InlineKeyboardMarkup()
g_inline_keyboard.add(types.InlineKeyboardButton('button1',callback_data=''))

scratch_url = 'https://scratch.mit.edu/projects/142394929'
back_inline = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('HMM GO BACK', callback_data='mainMenu'))
back_inline.add(types.InlineKeyboardButton('LINK to Scratch', url=scratch_url))



class MenuState(StatesGroup):
    menu = State()  

class FormRegistration(StatesGroup):
    name = State()  
    age = State()  
    money = State() 
    check = State() 

    




@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет пройди шаги регистрации по приколу!",reply_markup=greet_kb)
    await MenuState.menu.set()



@dp.message_handler(state=MenuState.menu)
async def echo(message: types.Message):
    if message.text == 'ЗАРЕГАТЬСЯ! 👋':
        await message.answer("Напиши свое имя:\n Желательно с Большой букви",reply_markup=types.ReplyKeyboardRemove())
        await FormRegistration.name.set()

@dp.message_handler(state=FormRegistration.name)
async def reg_name(message: types.Message, state: FSMContext):
    await message.reply(f'LOL😄 Тебя зовут: {message.text}, хотя я знаю тебя как {message.from_user.first_name} {message.from_user.last_name}!!\n Ну ти и Какашка!!')
    await message.reply(f'ОК, тогда напиши свой возраст {message.text}')
    await state.update_data(name=message.text)
    await FormRegistration.age.set()




@dp.message_handler(lambda message: message.text.isdigit(), state=FormRegistration.age)
async def process_age(message: types.Message, state: FSMContext):
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ОК, тогда Сколько у тебя денег малищЩЩ!!')
    await state.update_data(age=int(message.text))
    await FormRegistration.next()

@dp.message_handler(lambda message: message.text.isdigit(), state=FormRegistration.money)
async def process_money(message: types.Message, state: FSMContext):
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'ХАХАХАХАХХАХАХАХАХАХХАХА')
    await message.reply(f'Теряйся')
    await message.reply(f'Я забрал у тебя деньги!')
    await FormRegistration.next()
    async with state.proxy() as data:
        data['money'] = int(message.text)
        tt = f"""НУ значит {data.get('name')}
        Тебе {data.get('age')}
        Ну и у тебя 0 - {data.get('money')}
        C тебя 10000 доларов!
        Я знаю где ти живешь!!
        У тебя 10 часов!
        """
    back_inline = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Я всек понял с мне 10000 доларов', callback_data='YES'))
    await message.reply(f'Проверь правельно я тебя понял?')
    await message.answer(tt,reply_markup=back_inline)
    
@dp.callback_query_handler(lambda c: c.data == 'YES', state= FormRegistration.check)
async def progress_check(clq: types.CallbackQuery, state: FSMContext):
    await clq.message.reply(f'У тебя заканчиваеться времяяяяяяя!!!')
    await state.finish()
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



import logging
import json
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import random

logging.basicConfig(level=logging.INFO)

token = "2020284755:AAHyMBg0Wdd1BCB0GR2XvRvqa7_T3T1g7X8"
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop, storage=storage)



#ин лайн клавиатура для зарплаты
mainMenu = InlineKeyboardMarkup(row_width=2)
mainMenuDo25 = InlineKeyboardMarkup(row_width=2)
mainMenuBol25 = InlineKeyboardMarkup(row_width=2)
btnAge= InlineKeyboardButton(text='Ваш возраст ', callback_data="btnAge" )
btnDo25 = InlineKeyboardButton(text='Меньше 25 лет ', callback_data='btnDo25' )
btnDo25Agre = InlineKeyboardButton(text='Меньше 25 лет ✅ ', callback_data='btnDo25Agre' )
btnBol25 = InlineKeyboardButton(text='Больше 25 лет ',callback_data='btnBol25')
btnBol25Agre = InlineKeyboardButton(text='Больше 25 лет ✅',callback_data='btnBol25Agre')
btnBonus = InlineKeyboardButton(text='Бонусы за месяц ',callback_data='btnBonus' )
btnBonusVisit = InlineKeyboardButton(text="Посещаемость ", callback_data='btnBonusVisit' )
btnBonusMaster = InlineKeyboardButton(text="Master",callback_data='btnBonusMaster' )
btnBonusShift = InlineKeyboardButton(text="Shift leader",callback_data="btnBonusShift" )
btnBonusDiner = InlineKeyboardButton(text='Столовая',callback_data='btnBonusDiner' )
mainMenu.add(btnAge).row(btnDo25Agre,btnBol25).add(btnBonus).add(btnBonusVisit, btnBonusDiner, btnBonusMaster, btnBonusShift)
mainMenuDo25.add(btnAge).row(btnDo25Agre,btnBol25).add(btnBonus).add(btnBonusVisit, btnBonusDiner, btnBonusMaster, btnBonusShift)

mainMenuBol25.add(btnAge).row(btnDo25,btnBol25Agre).add(btnBonus).add(btnBonusVisit, btnBonusDiner, btnBonusMaster, btnBonusShift)

# mainMenu.add(btnBonus)
# mainMenu.add(btnBonusVisit, btnBonusDiner, btnBonusMaster, btnBonusShift)




# mainMenu.insert(btnDo25)
# mainMenu.insert(btnBol25)
# mainMenu.insert(btnBonus)
# mainMenu.insert(btnBonusVisit)
# mainMenu.insert(btnBonusDiner)
# mainMenu.insert(btnBonusMaster)
# mainMenu.insert(btnBonusShift)


@dp.message_handler(commands=['step'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,"Введите вашу почасовую оплату :",reply_markup=mainMenu )


@dp.callback_query_handler(text_contains= 'btn')
async def btnMain(call: types.CallbackQuery):
    if call.data == 'btnDo25':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите вашу почасовую оплату :",reply_markup=mainMenuDo25)
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите вашу почасовую оплату :",
                                    reply_markup=mainMenuBol25)
    # await bot.delete_message(call.from_user.id,call.message.message_id)
        print(call.data)

#отправка полседней новости всем
@dp.message_handler(commands='last')
async def start_join(message: types.Message):
    a=0
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)
        v = list(map(list, news_dict.items()))[-1][-1]
        news = f"<a href='{v['img']}'>&#8204;</a><a href='{v['current_url']}'><b>{v['title']}\n</b></a>\n{v['content']}"
        with open('bd.json', encoding="utf-8") as file:
            bd = json.load(file)
        for i in bd:
            try:
                await bot.send_message(chat_id=i, text=news)
                a+=1
            except Exception:
                pass
    print(f'{a} успешно отправленых сообщений')



# отправка меню по запросу
@dp.message_handler(commands='week_menu')
async def start_join(message: types.Message):
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)
        i = 0
        v = list(map(list, news_dict.items()))[-1][-1]
        while v['title'] != "Меню на тиждень":
            i -= 1
            v = list(map(list, news_dict.items()))[i - 1][-1]
        news = f"<a href='{v['img']}'>&#8204;</a><a href='{v['current_url']}'><b>{v['title']}\n</b></a>\n{v['content']}"
    await message.answer(news)




# создаём форму и указываем поля
class Form(StatesGroup):
    idcard = State()
    salary = State()
    dayday= State()
    custom = State()





# Начинаем наш диалог
@dp.message_handler(commands=['qrcode'])
async def qrcode(message: types.Message):
    await Form.idcard.set()
    await message.answer("Введите номер вашего пропуска:")

# рассчет зарплаты
@dp.message_handler(commands=['salary'])
async def salary(message: types.Message):
    await Form.salary.set()
    await message.answer("Введите вашу почасовую оплату:", reply_markup=mainMenu)

# отправка сообщения от имени бота
@dp.message_handler(commands=['custom'])
async def salary(message: types.Message):
    await Form.custom.set()
    await message.answer("Введи текст для отправки:")








#отмена задачи
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Задача была отменена')





#отправка кода на автобус
@dp.message_handler(state=Form.idcard)
async def process_age_invalid(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Вы ввели неверные данные. Для отмены нажмите /cancel или повторите ввод.")
    else:
        if len(message.text)==8:
            if message.text[:2]== '18' or message.text[:2]== '19' or message.text[:2]== '20' or message.text[:2]== '21' or message.text[:2]== '22' or message.text[:2]== '23':
                idcard = message.text
                qrcode = f"<a href='https://chart.googleapis.com/chart?chs=350x350&cht=qr&choe=UTF-8&chl={idcard}'>&#8204;</a>Ваш QR-код для проезда в автобусе"
                await message.reply(qrcode)
                await state.finish()
                print("Успушно созданый Qr code")
            else:
                await message.reply("Вы ввели неверные данные. Для отмены нажмите /cancel или повторите ввод.")
        else:
            await message.reply("Вы ввели неверные данные. Для отмены нажмите /cancel или повторите ввод.")





#принимаем оплату в чaс и запрашиваем количество отработаных дней
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.salary)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['salary'] = int(message.text)
    #await state.update_data(salary=int(message.text))
    await Form.next()
    await message.answer('Введите количество отработаных дней в порядке: дневные смены, ночные смены, дневные овертаймы, ночные овертаймы. \n Пример: 9,6,3,2 ')


# Сохраняем отработанные дни и выводим заработок
@dp.message_handler(state=Form.dayday)
async def process_gender(message: types.Message, state: FSMContext,):
    day = message.text.split(',')
    restoran = 47500
    bonus = 30000
    async with state.proxy() as data:
        try:
            if len(day) == 4:
                stavka=data['salary']*12
                daytime=int(day[0])
                nigtime = int(day[1])
                dayover = int(day[2])
                nigover = int(day[3])
                money = ((stavka * daytime + stavka * 2 * dayover) + (stavka * nigover * 2 + stavka * nigtime) + (stavka * nigover + stavka * nigtime) * 0.3 + restoran + bonus)*0.665
            else:
                raise
        except Exception:
            print('eror')
            await message.reply("Вы ввели неверные данные. Для отмены нажмите /cancel или повторите ввод.")
        else:
            await message.answer(f"Ориентировочный заработок с учетом столовой и бонуса за посещаемость: {int(money)} HUF")
            await state.finish()
            print("Успушно посчитаная зарплата")

#принимаю кастомные сообщения и отправляю всей базе подписиков
@dp.message_handler(state=Form.custom)
async def process_age(message: types.Message, state: FSMContext):
    with open('bd.json', encoding="utf-8") as file:
        bd = json.load(file)
    for i in bd:
        try:
            await bot.send_message(chat_id=i, text=message.text)
        except Exception:
            pass
    await state.finish()




# Проверяем число ли это
@dp.message_handler(lambda message: not message.text.isdigit(), state=(Form.idcard,Form.salary))
async def process_age_invalid(message: types.Message):
    return await message.reply("Вы ввели неверные данные. Для отмены нажмите /cancel или повторите ввод.")





if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
    loop.run_forever()


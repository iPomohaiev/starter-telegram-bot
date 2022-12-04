import logging
import json
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from main import news_check
import datetime
import random

logging.basicConfig(level=logging.INFO)

token = "2020284755:AAGoXRojX_n7hpvt18KIvdxbveT2koCCQLM"
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop, storage=storage)


#Отправка свежих новестей ботом
@dp.message_handler(commands='pars')
async def send_news(dp):
    await bot.send_message(chat_id="328455749", text="Парсинг запустился")
    while True:
        fresh_news = await news_check()
        if len(fresh_news) >= 1:
            time.sleep(2)
            for k, v in sorted(fresh_news.items()):
                news = f"<a href='{v['img']}'>&#8204;</a><a href='{v['current_url']}'><b>{v['title']}\n</b></a>\n{v['content']}"
                with open('bd.json', encoding="utf-8") as file:
                    bd = json.load(file)
                a=0
                for i in bd:
                    try:
                        await bot.send_message(chat_id=i, text=news)
                        a+=1
                    except Exception:
                        pass
                print(f'{a} успешно отправленых сообщений')
                await asyncio.sleep(10)
        else:
            while True:
                num_wek=datetime.datetime.now().strftime("%w")
                clock = datetime.datetime.now().strftime("%H")
                if num_wek =='1' or num_wek =='2' or num_wek =='3' or num_wek =='4' or num_wek =='5':
                    if clock=='9' or clock=='10' or clock=='11' or clock=='12' or clock=='13' or clock=='14' or clock=='15' or clock=='16':
                        rd_time=random.randint(3200, 3500)
                        print(f'"ждем около часа"+ {rd_time}')
                        await asyncio.sleep(rd_time)
                        break
                    else:
                        rd_time = random.randint(1600, 2000)
                        print(f'"ждем пол часа"+ {rd_time}')
                        await asyncio.sleep(rd_time)
                elif num_wek =='6' or num_wek =='0':
                    if clock=='9' or clock == '10' or clock == '11':
                        rd_time = random.randint(3200, 3600)
                        print(f'"ждем около часа"+ {rd_time}')
                        await asyncio.sleep(rd_time)
                        break
                    else:
                        rd_time = random.randint(1600, 2000)
                        print(f'"ждем пол часа"+ {rd_time}')
                        await asyncio.sleep(rd_time)

# отправка полследней новости из бвзы новому подписчику
@dp.message_handler(commands='start')
async def start_join(message: types.Message):
    user_id = str(message.chat.id)
    with open('bd.json', encoding="utf-8") as file:
        bd = json.load(file)
    if not user_id in bd:
        bd.append(user_id)
        numb = len(bd)
        await bot.send_message(chat_id="328455749", text=f"Новый подписчик номер {numb}")
    with open("bd.json", "w", encoding="utf-8") as file:
        json.dump(bd, file, indent=4, ensure_ascii=False)
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)
        d=0
        i=0
        while i<5:
            v = list(map(list, news_dict.items()))[-1-i-d][-1]
            while v['title'] == "Меню в ресторані":
                d += 1
                v = list(map(list, news_dict.items()))[-1-i-d][-1]
            news = f"<a href='{v['img']}'>&#8204;</a><a href='{v['current_url']}'><b>{v['title']}\n</b></a>\n{v['content']}"
            await message.answer(news)
            i += 1



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
# отправка меню по запросу
# @dp.message_handler(commands='week_menu')
# async def start_join(message: types.Message):
#     with open('news_dict.json', encoding="utf-8") as file:
#         news_dict = json.load(file)
#         i = 0
#         while True:
#             v = list(map(list, news_dict.items()))[i - 1][-1]
#             if v['title'] == "Меню тижня доступне в документах" or v['title'] == "Меню доступне в документах" or v['title'] == "Щотижневе меню доступне в документах":
#                 news = f"<a href='{v['img']}'>&#8204;</a><a href='{v['current_url']}'><b>{v['title']}\n</b></a>\n{v['content']}"
#                 break
#             else:
#                 i-=1
    # await message.answer(news)










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
    await message.answer("Введите вашу почасовую оплату:")

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
    # print("wait 10")
    # await message.answer(message.text)









# Проверяем число ли это
@dp.message_handler(lambda message: not message.text.isdigit(), state=(Form.idcard,Form.salary))
async def process_age_invalid(message: types.Message):
    return await message.reply("Вы ввели неверные данные. Для отмены нажмите /cancel или повторите ввод.")







#отправка кастомных сообщений от имени бота
# @dp.message_handler(commands='custom')
# async def start_join(message: types.Message):
#
#     with open('bd.json', encoding="utf-8") as file:
#         bd = json.load(file)
#     for i in bd:
#         news = [message.text.find(' ') : ]
#         print(news)
#         await bot.send_message(chat_id=i, text=news)



if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
    dp.loop.create_task(send_news(dp))
    loop.run_forever()


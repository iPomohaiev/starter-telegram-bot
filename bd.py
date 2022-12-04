import json


with open('bd.json', encoding="utf-8") as file:
    bd = json.load(file)

@bot.message_handler(commands=['start'])
async def startJoin(message: types.Message):
    if not str(message.chat.id) in bd:
        with open("bd.json", "w", encoding="utf-8") as file:
            json.dump(str(message.chat.id), file, indent=4, ensure_ascii=False)

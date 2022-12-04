from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import json
from schedule import every, repeat, run_pending
import asyncio
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
# фоновый режим
#options.add_argument("--headless")
url = 'https://app.hellosdi.hu/home/feed'
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#driver = webdriver.Chrome(options=options)
time.sleep(1)


# процес логинга на сайте

async def start():
    await asyncio.sleep(5)
    print('start')
    # for cookie in pickle.load(open("cookies", "rb")):
    #     driver.add_cookie(cookie)
    # await asyncio.sleep(2)
    # print("попытка логина под куки")
    # driver.refresh()
    # await asyncio.sleep(10)
    # driver.refresh()
    # await asyncio.sleep(5)
    # if driver.find_element_by_xpath("/html/body/main/div[3]/div/div[1]/div/a[1]"):
    #     pass
    # else:
    numInput = driver.find_element_by_id("input-19")
    numInput.clear()
    numInput.send_keys('19609707')
    pasInput = driver.find_element_by_id("input-20")
    pasInput.clear()
    pasInput.send_keys('182035Uu')
    await asyncio.sleep(1)
    pasInput.send_keys(Keys.ENTER)
    print("класический вход")
    await asyncio.sleep(10)
    # pickle.dump(driver.get_cookies(), open("cookies", "wb"))
    # print("сохранил новые куки")

    # driver.close()
    # driver.quit()


# получает артикл новости для сравнения
async def getArticl():
    await asyncio.sleep(5)
    current_url = driver.current_url
    articl_id = current_url.split('/')[-1]
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)
    return articl_id, news_dict


# меню тыжня с отправкой на pdf фаил
async def manuWeek(news_dict, articl_id, title):
    fresh_news_dict = {}
    driver.get('https://app.hellosdi.hu/documents/629ddc26-f679-4382-8851-8cae4f34b035')
    await asyncio.sleep(2)
    find_pdf = driver.find_element_by_class_name('fw-bold')
    find_pdf.click()
    await asyncio.sleep(5)
    src_img = driver.find_element_by_css_selector(
        "div.d-flex.card.bottom.bg-fill.justify-content-center.py-6 > a").get_attribute('href')
    print(src_img)
    current_url = driver.current_url
    content = ""
    await asyncio.sleep(3)
    news_dict[articl_id] = {
        'current_url': current_url,
        'title': title,
        'content': content,
        'img': src_img
    }
    fresh_news_dict[articl_id] = {
        'current_url': current_url,
        'title': title,
        'content': content,
        'img': src_img
    }

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    print('Сохранил новость')
    driver.get(url=url)
    await asyncio.sleep(10)
    return fresh_news_dict


# парсим новость
async def news(news_dict, articl_id, current_url, title):
    print('парсим описание')
    fresh_news_dict = {}
    await asyncio.sleep(5)
    try:
        contents = driver.find_element_by_class_name("col-12.col-lg-8.offset-lg-2.mt-3")
        content = contents.text
    except:
        content = ""
    try:
        src_imgs = driver.find_element_by_xpath("/html/body/div[1]/main/div[3]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div/div/figure/a/img")
         
        src_img = src_imgs.get_attribute('src')
    except:
        try:
            src_imgs = driver.find_element_by_xpath(
                "/html/body/main/div[3]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div/div[3]/figure/a/img")
            src_img = src_imgs.get_attribute('src')
        except:
            try:
                src_imgs = driver.find_element_by_css_selector("div.image-wrapper > img")
                src_img = src_imgs.get_attribute('src')
            except:
                try:
                    src_imgs = driver.find_element_by_xpath("/html/body/div/main/div[3]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div/div/figure/a/img")
                    src_img = src_imgs.get_attribute('src')
                except:
                    src_img = ""

    """
    try:
        contents = driver.find_element_by_class_name("col-12.col-lg-8.offset-lg-2.mt-3")
        try:
            src_imgs = driver.find_element_by_css_selector("div.image-wrapper > img")
        except Exception:
            src_imgs = driver.find_element_by_xpath(
            "/html/body/main/div[3]/div/div[2]/div[2]/section/div/div/div[3]/div/div/div/div[3]/figure/a/img")
    except Exception:
        driver.refresh()
        await asyncio.sleep(5)
    else:
        content = contents.text
        src_img = src_imgs.get_attribute('src')
        """
    print(content)
    print(src_img)

    await asyncio.sleep(5)
    news_dict[articl_id] = {
        'current_url': current_url,
        'title': title,
        'content': content,
        'img': src_img
    }
    fresh_news_dict[articl_id] = {
        'current_url': current_url,
        'title': title,
        'content': content,
        'img': src_img
    }

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    await asyncio.sleep(1)
    driver.get(url=url)
    print('Сохранил новость')
    await asyncio.sleep(10)
    return fresh_news_dict

# пропускаем меню в новом ресторане на каджый день
# async def menu_evry_day(news_dict, articl_id, current_url, title):
#     print('пропускаем')
#     await asyncio.sleep(5)
#     fresh_news_dict = {}
#     driver.get(url=url)
#     await asyncio.sleep(4)
#     content = ""
#     src_img = ""
#     news_dict[articl_id] = {
#         'current_url': current_url,
#         'title': title,
#         'content': content,
#         'img': src_img
#     }
#     with open("news_dict.json", "w", encoding="utf-8") as file:
#         json.dump(news_dict, file, indent=4, ensure_ascii=False)
#     await asyncio.sleep(5)
#     return fresh_news_dict


# возврат списка с новыми новостями если таковы есть
async def news_check():
    driver.get(url=url)
    await asyncio.sleep(5)
    # проверка и вход если найден елемент с страницы логина
    while True:
        try:
            driver.find_element_by_id("input-19")
            await start()
        except Exception:
            break
        else:
            break
    # # driver.get(url='https://app.hellosdi.hu/view/posts/1d84c615-dabf-4e01-ac8f-2c5d35464e81')
    # # проверка загрузились ли заголовки новостей на главной
    # await asyncio.sleep(5)
    # while True:
    #     try:
    #         driver.find_elements_by_class_name("content-block.card.mb-4")
    #     except Exception:
    #         driver.get(url=url)
    #         await asyncio.sleep(5)
    #     else:
    #         break
    # name = driver.find_element_by_class_name("title")
    # name.click()
    print("try")

    fresh_news1={}
    await asyncio.sleep(5)

    for i in range(0, 3):
        col_relod = 0
        await asyncio.sleep(10)
        while True:
            if col_relod<3:
                try:
                    driver.get(url=url)
                    await asyncio.sleep(15)
                    names = driver.find_elements_by_class_name("title")
                    await asyncio.sleep(5)
                    if names[i].text == "Actual":
                        break

                    print(names[i].text)
                    names[i].click()
                    await asyncio.sleep(25)
                    current_url = driver.current_url
                    articl_id = current_url.split('/')[-1]
                    with open('news_dict.json', encoding="utf-8") as file:
                        news_dict = json.load(file)
                    if articl_id in news_dict:
                        driver.get(url=url)
                        print('Это не новая новость')
                        await asyncio.sleep(3)
                        break
                    else:
                        await asyncio.sleep(5)
                        title = driver.find_element_by_css_selector("h1.text-center").text
                        print(title)
                        if title == "Меню тижня доступне в документах" or title=="Меню доступне в документах" or title == "Щотижневе меню доступне в документах":
                            title = "Меню на тиждень"
                            fresh_news=await manuWeek(news_dict, articl_id, title)
                        # elif title == "Меню в ресторані" or title == "Меню в новому ресторані" or title=="Сьогоднішнє меню":
                        #     fresh_news=await menu_evry_day(news_dict, articl_id, current_url, title)

                        elif title == "" or title == " ":
                            raise print("пустой заголовок")

                        else:
                            fresh_news= await news(news_dict, articl_id, current_url, title)

                        await asyncio.sleep(10)
                        fresh_news1.update(fresh_news)

                except Exception:
                    driver.get(url=url)
                    print('ошибка загрузки страницы')
                    col_relod+=1
                    print(f'ошибка загрузки страницы. Попітеа № {col_relod}')
                    await asyncio.sleep(10)
                else:
                    break
            else:
                break
    print("Новостей нет!")


    return fresh_news1
    # loop.run_until_complete(news_check())
    # loop.run_forever()

    print("Gotovo")

    # return fresh_news_dict

# while True:
#     run_pending()
#     await asyncio.sleep(1)

print("Start")
# loop = asyncio.get_event_loop()







# schedule.every(120).seconds.do(news_check())
# while True:
#     schedule.run_pending()
#     await asyncio.sleep(1)

# Вклвдка на которой видно размерфайла и можно выбрать его
# https://app.hellosdi.hu/documents/629ddc26-f679-4382-8851-8cae4f34b035
# вкладка с которой можно скачать файл
# https://app.hellosdi.hu/documents/view/ef3e1b81-3527-43b1-8bc6-e31af31f7e6a
# <div data-v-0e9d90a2 class="cancel">
#
# <i data-v-0e9d90a2 class ="fa fa-times-circle fs-30 text-white cursor-pointer ml-auto" >
#
# < header data-v-0e9d90a2 class ="d-flex flex-column flex-lg-row align-items-center" > … < / header > flex
#
# < div data-v-0e9d90a2 class ="div" >
#
# < h1 data-v-0e9d90a2 class ="m-0 text-white text-center" > Отримали нове оповіщення < / h1 >
# http://support.samsung.net/static/supportai/appDownloadPopup.html
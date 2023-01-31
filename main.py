import os
import requests
from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

 
bot = Bot(os.getenv("AIOTOKEN"))
dp = Dispatcher(bot)
 
 
@dp.message_handler(commands=['start', 'help'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, """
Привет! Я бот, который поможет быстро находить ключи для игр стим на <b><a href="https://hot-game.info"> hot-game.info </a></b>

Для того, чтобы я отправил тебе цену на ключ, введи в поле его название игры(Напишите правильное название игры иначе бот не будет работать.)""",
parse_mode="HTML", disable_web_page_preview=1)#отключать просмотр картинтинки сайта)

#парсер 
@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    url = "https://hot-game.info/q=" + message.text #ссылка на сайт
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser") 

 
    links = soup.find("div", class_="mw-search-result-heading")

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
 
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    
    driver.execute_script("window.scrollTo(0, 200)")
    driver.save_screenshot("img.png")
    driver.close()
 
    photo = open("img.png", 'rb') #картинка сайта
    #отправка пользователю
    await bot.send_photo(message.chat.id, photo=photo, caption=f'Ссылка на сайт: <a href="{url}">тык</a>', parse_mode="HTML")
 
 
 
executor.start_polling(dp)
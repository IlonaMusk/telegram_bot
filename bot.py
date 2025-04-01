#!/usr/local/bin/python3
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from webdriver_manager.chrome import ChromeDriverManager


# Telegram токен и ID чата (замени на свои)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Функция для проверки дат
async def check_dates():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без UI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    chrome_driver_path = "/opt/homebrew/bin/chromedriver"  # Укажи свой путь
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/#/")
        time.sleep(3)  # Даем странице загрузиться

        # Выбираем отделение
        driver.find_element(By.XPATH, '//*[@id="step1"]/div/div[2]/div/div/div/div/div/div/div[4]/div/div').click()
        time.sleep(2)

        # Выбираем услугу
        driver.find_element(By.XPATH, '//*[@id="step2"]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div/div').click()
        time.sleep(2)

        # Нажимаем на кнопку даты
        driver.find_element(By.XPATH, '//*[@id="dateTimeHeading"]').click()
        time.sleep(3)

        # Проверяем наличие текста "Obecnie nie ma wolnych terminów"
        no_dates_text = "Obecnie nie ma wolnych terminów. Proszę spróbować później."
        result = driver.find_elements(By.XPATH, '//*[@id="step3"]/div/div/div/div/div[3]/div/div')

        if result and no_dates_text in result[0].text:
            print("Нет свободных дат")
        else:
            print("Есть свободные даты!")
            await bot.send_message(CHAT_ID, "🔔 Свободные даты появились! Проверь сайт!")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.quit()

# Запускаем проверку каждые 5 минут
async def scheduler():
    while True:
        await check_dates()
        await asyncio.sleep(300)  # 5 минут

# Запуск бота
async def main():
    await bot.send_message(CHAT_ID, "✅ Бот запущен и мониторит даты")
    await scheduler()

if __name__ == "__main__":
    asyncio.run(main())

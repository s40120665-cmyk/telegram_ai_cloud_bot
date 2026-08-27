import os
import telebot
import requests
from io import BytesIO

# Твой рабочий токен Telegram-бота
BOT_TOKEN = "8826304105:AAGPg7LX8OAF7InzK5jfWgMRDCGZZ__IysU"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я твой персональный ИИ-ассистент.\n\n"
        "💬 Просто пиши мне любые вопросы, и я буду отвечать.\n\n"
        "🎨 Чтобы сгенерировать картинку, используй команду:\n"
        "`/image твой запрос` (например: `/image котик в космосе`)"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['image'])
def generate_image(message):
    prompt = message.text.replace("/image", "").strip()
    if not prompt:
        bot.reply_to(message, "Пожалуйста, напиши описание картинки после команды. Пример: `/image красный автомобиль`")
        return
        
    bot.reply_to(message, "⏳ Генерирую изображение, подожди пару секунд...")
    
    # Новый неубиваемый шлюз для картинок
    url = f"https://api.aiyana.dev/image?p={requests.utils.quote(prompt)}"
    
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            bot.send_photo(message.chat.id, res.content, caption=f"🎨 Ваш запрос: {prompt}")
        else:
            bot.reply_to(message, "Не удалось сгенерировать картинку. Попробуй позже.")
    except:
        bot.reply_to(message, "Ошибка при создании изображения.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Новый рабочий текстовый шлюз без блокировок хостинга
    url = f"https://api.aiyana.dev/chat?q={requests.utils.quote(message.text)}"
    
    try:
        res = requests.get(url, timeout=20)
        if res.status_code == 200 and res.text:
            bot.reply_to(message, res.text)
        else:
            bot.reply_to(message, "Извини, нейросеть сейчас занята. Попробуй позже!")
    except:
        bot.reply_to(message, "Произошла ошибка при подключении к ИИ.")

if __name__ == "__main__":
    print("Бот успешно запущен!")
    bot.infinity_polling()

import os
import telebot
import requests

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
    
    # 100% правильный URL для точной генерации картинок Flux без блокировок
    image_url = "https://image.pollinations.ai/p/" + requests.utils.quote(prompt) + "?width=1024&height=1024&nologo=true"
    
    try:
        img_data = requests.get(image_url, timeout=30).content
        bot.send_photo(message.chat.id, img_data, caption=f"🎨 Ваш запрос: {prompt}")
    except Exception as e:
        bot.reply_to(message, "Не удалось сгенерировать картинку. Попробуй другое описание.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    # 100% правильный и бесплатный URL для текста без лимитов и блокировок
    url = f"https://api.aiyana.dev/chat?q={requests.utils.quote(message.text)}"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Извини, нейросеть сейчас занята. Попробуй позже!")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при подключении к ИИ.")

if __name__ == "__main__":
    print("Бот успешно запущен!")
    bot.infinity_polling()

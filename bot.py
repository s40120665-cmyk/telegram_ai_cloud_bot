import os
import telebot
import requests

# Твой токен вшит прямо в код
BOT_TOKEN = "8826304105:AAGPg7LX8OAF7InzK5jfWgMRDCGZZ__IysU"
bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище истории диалогов {chat_id: [список сообщений]}
chat_histories = {}

def get_ai_response(chat_id, user_text):
    """Функция для работы с текстовым ИИ (с памятью контекста)"""
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    
    # Добавляем новое сообщение пользователя в историю
    chat_histories[chat_id].append({"role": "user", "content": user_text})
    
    # Ограничиваем память последними 6 сообщениями, чтобы сервер не перегружался
    if len(chat_histories[chat_id]) > 6:
        chat_histories[chat_id] = chat_histories[chat_id][-6:]
        
    # Формируем запрос к бесплатному ИИ
    url = "https://pollinations.ai"
    payload = {
        "messages": chat_histories[chat_id],
        "model": "openai" # Используем продвинутую модель
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            ai_text = response.text
            # Сохраняем ответ ИИ в историю для контекста
            chat_histories[chat_id].append({"role": "assistant", "content": ai_text})
            return ai_text
        return "Извини, нейросеть сейчас занята. Попробуй позже!"
    except Exception as e:
        return "Произошла ошибка при подключении к ИИ."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я твой персональный ИИ-ассистент.\n\n"
        "💬 **Просто пиши мне любые вопросы**, и я буду отвечать, удерживая контекст беседы.\n\n"
        "🎨 Чтобы **сгенерировать картинку**, используй команду:\n"
        "`/image твой запрос` (например: `/image котик в космосе`)"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['image'])
def generate_image(message):
    # Отрезаем саму команду /image, оставляя только промпт
    prompt = message.text.replace("/image", "").strip()
    
    if not prompt:
        bot.reply_to(message, "Пожалуйста, напиши описание картинки после команды. Пример: `/image красный автомобиль`")
        return
        
    bot.reply_to(message, "⏳ Генерирую изображение, подожди пару секунд...")
    
    # Формируем ссылку на бесплатный генератор картинок Flux
    image_url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true"
    
    try:
        # Скачиваем сгенерированную картинку в память сервера и отправляем в телеграм
        img_data = requests.get(image_url, timeout=20).content
        bot.send_photo(message.chat.id, img_data, caption=f"🎨 Ваш запрос: {prompt}")
    except Exception as e:
        bot.reply_to(message, "Не удалось сгенерировать картинку. Попробуй другое описание.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Показываем статус "печатает...", пока ИИ думает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Получаем ответ от ИИ
    answer = get_ai_response(message.chat.id, message.text)
    
    # Отправляем ответ пользователю
    bot.reply_to(message, answer)

# Запуск бота в бесконечном цикле
if __name__ == "__main__":
    print("Бот успешно запущен в облаке!")
    bot.infinity_polling()

import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = '8817689128:AAFhxQCpaOAuwYvUk7vxFvIi2Yv9gQUlJ1I'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Пришли мне ссылку на видео (TikTok, Reels, YouTube), и я попробую его скачать и отправить тебе.")

@bot.message_handler(func=lambda message: message.text.startswith('http'))
def download_and_send_video(message):
    url = message.text
    status_msg = bot.send_message(message.chat.id, "🔄 Начинаю скачивание видео, подождите...")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloaded_video.mp4',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists('downloaded_video.mp4'):
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass
            
            with open('downloaded_video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video, caption="Вот твое видео! 🎬")
            
            os.remove('downloaded_video.mp4')
        else:
            bot.send_message(message.chat.id, "❌ Не удалось сохранить файл видео.")

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "❌ Ошибка при скачивании. Возможно, ссылка не поддерживается или профиль автора закрыт.")
        if os.path.exists('downloaded_video.mp4'):
            os.remove('downloaded_video.mp4')

print("Бот успешно запущен и готов к работе!")
bot.infinity_polling(timeout=10, long_polling_timeout=5)

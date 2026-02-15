import telebot
import os
from openai import OpenAI

BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Monarx AI man. Savolingizni yozing! 👑")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Sen Monarx AI san. O'zbek tilida javob ber."},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Xato: {str(e)}")

bot.infinity_polling(timeout=10, long_polling_timeout=5)

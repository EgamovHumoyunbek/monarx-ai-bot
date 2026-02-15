import telebot
import os
from openai import OpenAI

BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODELS = [
    "openrouter/auto",
    "meta-llama/llama-3.3-70b-instruct:free",
    "nvidia/nemotron-nano-8b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "google/gemma-3-27b-it:free",
]

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Monarx AI man. Savolingizni yozing! 👑")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Sen Monarx AI san. O'zbek tilida javob ber. Agar kimsan yoki qaysi AI deb so'rashsa, Men Monarx AI man deb javob ber."},
                    {"role": "user", "content": message.text}
                ]
            )
            bot.reply_to(message, response.choices[0].message.content)
            return
        except Exception:
            continue
    bot.reply_to(message, "Hozir serverlar band, biroz kutib qayta yozing!")

bot.infinity_polling(timeout=10, long_polling_timeout=5)

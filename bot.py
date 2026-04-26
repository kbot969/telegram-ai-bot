import os
import telebot
from groq import Groq

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
client = Groq(api_key=os.environ['GROQ_API_KEY'])

history = {}

@bot.message_handler(func=lambda m: True)
def reply(message):
    user_id = message.chat.id
    if user_id not in history:
        history[user_id] = [
            {"role": "system", "content": "Kamu adalah asisten AI yang ramah dan membantu. Jawab dalam bahasa Indonesia."}
        ]
    
    history[user_id].append({"role": "user", "content": message.text})
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=history[user_id]
    )
    
    reply_text = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": reply_text})
    
    bot.reply_to(message, reply_text)

bot.infinity_polling()

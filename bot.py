BOT_SCRIPT = """  
import telebot, time  

TOKEN = "7949052497:AAH9yNI0bU4bmf4wAcgegfZaKxbrSvgm9QI"  
bot = telebot.TeleBot(TOKEN)  

@bot.message_handler(commands=['start'])  
def start(message):  
    bot.send_message(message.chat.id, "Bot is running!")  

while True:  
    try:  
        bot.polling(non_stop=True)  
    except Exception as e:  
        print(f"Bot crashed: {e}")  
        time.sleep(5)  
"""

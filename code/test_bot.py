import telebot


bot = telebot.TeleBot("7625281184:AAFLX1EbK2Ec8Pq4U-7GRLv1RJZjni6hbF4")
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"Received message: {message.text}")
    bot.reply_to(message, f"You said: {message.text}")


try:
    print("Starting bot polling...")
    bot.polling(non_stop=True)
except Exception as e:
    print(f"Error in polling: {e}")

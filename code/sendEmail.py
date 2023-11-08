import helper
import logging
from tabulate import tabulate

# === Documentation of history.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. It calls helper.py to get the user's
    historical data and based on whether there is data available, it either prints an error message or
    displays the user's historical data.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        table = [["Date", "Category", "Amount"]]
        if user_history is None:
            raise Exception("Sorry! No spending records found!")
        if len(user_history) == 0:
            raise Exception("Sorry! No spending records found!")
        else:
            for rec in user_history:
                values = rec.split(',')
                # Store each value in separate variables
                date, category, amount = values
                table.append([date, category, "$ " + amount])
            s = io.StringIO()
            csv.writer(s).writerows(table)
            s.seek(0)
            buf = io.BytesIO()
            buf.write(s.getvalue().encode())
            buf.seek(0)
            buf.name = "history.csv"
            # bot.send_document(chat_id, buf)
            # category = bot.reply_to(message, "Enter category name")
            category = bot.send_message(message.chat.id, "Enter your email id")
            bot.register_next_step_handler(category, acceptEmailId)        

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))
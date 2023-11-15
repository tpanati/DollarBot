import helper
import telebot

def run(message, bot):

    chat_id = message.chat.id

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Add new category")
    markup.add("Edit category")
    markup.add("Delete category")

    msg = bot.send_message(chat_id, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_messages, bot)

def handle_messages(message, bot):
    chat_id = message.chat.id
    msg = message.text

    if msg == "Add new category":
        message1 = bot.send_message(chat_id, "Please enter your category")
        bot.register_next_step_handler(message1, post_add_category, bot)
    elif msg == "Delete category":
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for c in helper.getSpendCategories():
            markup.add(c)
        message1 = bot.reply_to(message, "Select Category to delete", reply_markup=markup)
        bot.register_next_step_handler(message1, post_delete_category, bot)
    elif msg == "Edit category":
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for c in helper.getSpendCategories():
            markup.add(c)
        message1 = bot.reply_to(message, "Select Category to edit", reply_markup=markup)
        bot.register_next_step_handler(message1, post_edit_category, bot)


def post_add_category(message, bot):
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if selected_category not in allocated_categories.keys():
        helper.updateBudgetCategory(chat_id,selected_category)
    helper.spend_categories.insert(0,selected_category)
    bot.send_message(chat_id, "Category successfully added!")

def post_delete_category(message, bot):
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if selected_category in allocated_categories.keys():
        helper.deleteBudgetCategory(chat_id, selected_category)
    if selected_category in helper.spend_categories:
        helper.spend_categories.remove(selected_category)
    bot.send_message(chat_id, "Category successfully deleted!")

def post_edit_category(message, bot):
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if selected_category in allocated_categories.keys():
        helper.deleteBudgetCategory(chat_id, selected_category)
    if selected_category in helper.spend_categories:
        helper.spend_categories.remove(selected_category)
    message1 = bot.send_message(chat_id, "Please enter the new name for the category you want to edit")
    bot.register_next_step_handler(message1, post_add_category, bot)
import helper
from telebot import types

def run(message, bot):

    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Add new category")
    markup.add("Edit category")
    markup.add("Delete category")
    msg = bot.reply_to(message, "Select Category", reply_markup=markup).text

    if msg == "Add new category":
        message1 = bot.send_message(chat_id, "Please enter your category")
        post_add_category(message1)
        bot.send_message(chat_id, "Category successfully added!")
    elif msg == "Delete category":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for c in helper.getSpendCategories():
            markup.add(c)
        message1 = bot.reply_to(message, "Select Category to delete", reply_markup=markup)
        post_delete_category(message1)
        bot.send_message(chat_id, "Category successfully deleted!")

def post_add_category(message):
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if selected_category not in allocated_categories.keys():
        helper.updateBudgetCategory(chat_id,selected_category)
    helper.spend_categories.insert(0,selected_category)


def post_delete_category(message):
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if selected_category in allocated_categories.keys():
        helper.deleteBudgetCategory(chat_id, selected_category)
    helper.spend_categories.remove(selected_category)

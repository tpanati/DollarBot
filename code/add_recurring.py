"""
File: add_recurring.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import helper
import logging
from telebot import types
from datetime import datetime
from dateutil.relativedelta import relativedelta
from exception import InvalidCategoryError, InvalidAmountError, InvalidDurationError

option = {}


def run(message, bot):
    """
    run(message, bot): Initializes the expense recording process by presenting the user with a list of spend categories.
    
    Parameters:
    - message (telegram.Message): The message object received from the user.
    - bot (telegram.Bot): The Telegram bot object.
    """

    helper.read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


def post_category_selection(message, bot):

    """
    post_category_selection(message, bot): Processes the user's selected expense category and prompts for the expense amount.

    Parameters:
    - message (telegram.Message): The message object received from the user.
    - bot (telegram.Bot): The Telegram bot object.

    Raises:
    - Exception: If the selected category is not recognized.
    """

    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise InvalidCategoryError(selected_category, "I don’t recognize this category")

        option[chat_id] = selected_category
        message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only)'.format(str(option[chat_id])))
        bot.register_next_step_handler(message, post_amount_input, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        commands = helper.getCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def post_amount_input(message, bot, selected_category):
    """
    post_amount_input(message, bot, selected_category): Processes the user's entered expense amount and prompts for the duration.

    Parameters:
    - message (telegram.Message): The message object received from the user.
    - bot (telegram.Bot): The Telegram bot object.
    - selected_category (str): The selected expense category.

    Raises:
    - Exception: If the entered amount is invalid or $0.
    """
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise InvalidAmountError("Spent amount has to be a non-zero number.")

        message = bot.send_message(chat_id, 'For how many months in the future will the expense be there? \n(Enter integer values only)')
        bot.register_next_step_handler(message, post_duration_input, bot, selected_category, amount_value)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))


def post_duration_input(message, bot, selected_category, amount_value):
    
    """
    post_duration_input(message, bot, selected_category, amount_value): Processes the user's entered duration and records the expense.

    Parameters:
    - message (telegram.Message): The message object received from the user.
    - bot (telegram.Bot): The Telegram bot object.
    - selected_category (str): The selected expense category.
    - amount_value (float): The entered expense amount.

    Raises:
    - Exception: If the entered duration is invalid or 0.
    """
    try:
        chat_id = message.chat.id
        duration_entered = message.text
        duration_value = helper.validate_entered_duration(duration_entered)
        if duration_value == 0:
            raise InvalidDurationError("Duration has to be a non-zero integer.")
                
        for i in range(int(duration_value)):
            date_of_entry = (datetime.today().date() + relativedelta(months=+i)).strftime(helper.getDateFormat())
            date_str, category_str, amount_str = str(date_of_entry), str(selected_category), str(amount_value)
            helper.write_json(add_user_record(chat_id, "{},{},{}".format(date_str, category_str, amount_str)))
        
        bot.send_message(chat_id, 'The following expenditure has been recorded: You have spent ${} for {} for the next {} months'.format(amount_str, category_str, duration_value))
    
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))

def add_user_record(chat_id, record_to_be_added):

    """
    add_user_record(chat_id, record_to_be_added): Adds a new expense record to the user's data.

    Parameters:
    - chat_id (int): The user's chat ID.
    - record_to_be_added (str): The expense record to be added in CSV format.

    Returns:
    dict: Updated user data dictionary.
    """

    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    user_list[str(chat_id)]['data'].append(record_to_be_added)
    return user_list

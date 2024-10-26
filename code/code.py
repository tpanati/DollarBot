"""
File: code.py
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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import edit
import history
import pdf
import display
import estimate
import delete
import add
import budget
import analytics
import predict
import updateCategory
import weekly
import monthly
import sendEmail
import add_recurring
import os
import tempfile
import speech_recognition as sr
from datetime import datetime
from jproperties import Properties
from pydub import AudioSegment
from telebot import types


configs = Properties()

with open("user.properties", "rb") as read_prop:
    configs.load(read_prop)

api_token = str(configs.get("api_token").data)

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}
user_list = {}

# === Documentation of code.py ===

# Define listener for requests by user
def listener(user_requests):
    """
    listener(user_requests): Takes 1 argument user_requests and logs all user
    interaction with the bot including all bot commands run and any other issue logs.
    """
    for req in user_requests:
        if req.content_type == "text":
            print(
                "{} name:{} chat_id:{} \nmessage: {}\n".format(
                    str(datetime.now()),
                    str(req.chat.first_name),
                    str(req.chat.id),
                    str(req.text),
                )
            )

    message = (
        ("Sorry, I can't understand messages yet :/\n"
         "I can only understand commands that start with /. \n\n"
         "Type /faq or /help if you are stuck.")
    )

    try:
        helper.read_json()
        chat_id = user_requests[0].chat.id

        if user_requests[0].text[0] != "/":
            bot.send_message(chat_id, message)
    except Exception:
        pass

bot.set_update_listener(listener)

@bot.message_handler(commands=["help"])
def show_help(m):
    chat_id = m.chat.id
    message = (
        "*Here are the commands you can use:*\n"
        "/add - Add a new expense 💵\n"
        "/history - View your expense history 📜\n"
        "/budget - Check your budget 💳\n"
        "/analytics - View graphical analytics 📊\n"
        "For more info, type /faq or tap the button below 👇"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("FAQ", callback_data='faq'))
    bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(commands=["faq"])
def faq(m):

    helper.read_json()
    chat_id = m.chat.id

    faq_message = (
        ('"What does this bot do?"\n'
         ">> DollarBot lets you manage your expenses so you can always stay on top of them! \n\n"
         '"How can I add an epxense?" \n'
         ">> Type /add, then select a category to type the expense. \n\n"
         '"Can I see history of my expenses?" \n'
         ">> Yes! Use /analytics to get a graphical display, or /history to view detailed summary.\n\n"
         '"I added an incorrect expense. How can I edit it?"\n'
         ">> Use /edit command. \n\n"
         '"Can I check if my expenses have exceeded budget?"\n'
         ">> Yes! Use /budget and then select the view category. \n\n")
    )
    bot.send_message(chat_id, faq_message)

# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=["start", "menu"])
def start_and_menu_command(m):
    helper.read_json()
    chat_id = m.chat.id
    text_intro = (
        "*Welcome to the Dollar Bot!* \n"
        "DollarBot can track all your expenses with simple and easy-to-use commands :) \n"
        "Here is the complete menu:\n\n"
    )

    commands = helper.getCommands()
    keyboard = types.InlineKeyboardMarkup()

    for command, description in commands.items():
        button_text = f"/{command}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=command))

    text_intro += "_Click a command button to use it._"
    bot.send_message(chat_id, text_intro, reply_markup=keyboard, parse_mode='Markdown')
    return True

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Handles button clicks and executes the corresponding command actions.
    """
    command = call.data  # The command from the button clicked

    # Check which command was clicked and perform the corresponding action
    if command == "help":
        show_help(call.message)
    elif command == "pdf":
        command_pdf(call.message)
    elif command == "add":
        command_add(call.message)
    elif command == "menu":
        start_and_menu_command(call.message)
    elif command == "add_recurring":
        command_add_recurring(call.messsage)
    elif command == "analytics":
        command_analytics(call.message)
    elif command == "predict":
        command_predict(call.message)
    elif command == "history":
        command_history(call.message)
    elif command == "delete":
        command_delete(call.message)
    elif command == "display":
        command_display(call.message)
    elif command == "edit":
        command_edit(call.message)
    elif command == "budget":
        command_budget(call.message)
    elif command == "updateCategory":
        command_updateCategory(call.message)
    elif command == "weekly":
        command_weekly(call.message)
    elif command == "monthly":
        command_monthly(call.message)
    elif command == "sendEmail":
        command_sendEmail(call.message)
    else:
        response_text = "Command not recognized."

    # Acknowledge the button press
    # Acknowledge the button press
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

# defines how the /add command has to be handled/processed
@bot.message_handler(commands=["add"])
def command_add(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    add.run(message, bot)

# defines how the /weekly command has to be handled/processed
@bot.message_handler(commands=["weekly"])
def command_weekly(message):
    """
    command_weekly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls weekly.py to run to execute
    the weekly analysis functionality. Commands used to run this: commands=['weekly']
    """
    weekly.run(message, bot)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    # Get the voice file
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Create a temporary OGG file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_ogg:
        temp_ogg.write(downloaded_file)
        temp_ogg_path = temp_ogg.name

    # Convert OGG to WAV
    temp_wav_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
    audio = AudioSegment.from_ogg(temp_ogg_path)
    audio.export(temp_wav_path, format='wav')

    # Use SpeechRecognition to convert voice to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            bot.send_message(message.chat.id, f"I heard: \"{text}\"")
            process_command(text, message)
        except sr.UnknownValueError:
            bot.reply_to(message, "Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            bot.reply_to(message, "Could not request results from the speech recognition service.")

    # Cleanup: remove the temporary files
    os.remove(temp_ogg_path)
    os.remove(temp_wav_path)

def process_command(text, message):
    if "expense" in text:
        command_add(message)
    elif "history" in text:
        command_history(message)  # Call the existing history command
    elif "budget" in text:
        command_budget(message)  # Call the existing budget command
    elif "menu" in text:
        start_and_menu_command(message)
    elif "help" in text:
        show_help(message)
    elif "weekly" in text:
        command_weekly(message)
    elif "monthly" in text:
        command_monthly(message)
    elif "predict" in text:
        command_predict(message)
    else:
        bot.send_message(message.chat.id, "I didn't recognize that command.")
        
# defines how the /monthly command has to be handled/processed
@bot.message_handler(commands=["monthly"])
def command_monthly(message):
    """
    command_monthly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls monthly.py to run to execute
    the monthly analysis functionality. Commands used to run this: commands=['monthly']
    """
    monthly.run(message, bot)

#handles add_recurring command
@bot.message_handler(commands=['add_recurring'])
def command_add_recurring(message):
    add_recurring.run(message, bot)

# handles pdf command
@bot.message_handler(commands=["pdf"])
def command_pdf(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls pdf.py to run to execute
    the add functionality. Commands used to run this: commands=['pdf']
    """
    pdf.run(message, bot)

#handles updateCategory command
@bot.message_handler(commands=["updateCategory"])
def command_updateCategory(message):
    """
    command_updateCategory(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls updateCategory.py to run to execute
    the updateCategory functionality. Commands used to run this: commands=['updateCategory']
    """
    updateCategory.run(message, bot)

# function to fetch expenditure history of the user
@bot.message_handler(commands=["history"])
def command_history(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls history.py to run to execute
    the add functionality. Commands used to run this: commands=['history']
    """
    history.run(message, bot)

# function to fetch expenditure history of the user
@bot.message_handler(commands=["sendEmail"])
def command_sendEmail(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls sendEmail.py to run to execute
    the sending an email of the expense history. Commands used to run this: commands=['sendEmail']
    """
    sendEmail.run(message, bot)

# function to edit date, category or cost of a transaction
@bot.message_handler(commands=["edit"])
def command_edit(message):
    """
    command_edit(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls edit.py to run to execute
    the add functionality. Commands used to run this: commands=['edit']
    """
    edit.run(message, bot)

# function to display total expenditure
@bot.message_handler(commands=["display"])
def command_display(message):
    """
    command_display(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls display.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    display.run(message, bot)

# function to estimate future expenditure
@bot.message_handler(commands=["estimate"])
def command_estimate(message):
    """
    command_estimate(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['estimate']
    """
    estimate.run(message, bot)

# handles "/delete" command
@bot.message_handler(commands=["delete"])
def command_delete(message):
    """
    command_delete(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    delete.run(message, bot)

# handles budget command
@bot.message_handler(commands=["budget"])
def command_budget(message):
    budget.run(message, bot)

# handles analytics command
@bot.message_handler(commands=["analytics"])
def command_analytics(message):
    """
    command_analytics(message): Take an argument message with content and chat ID. Calls analytics to 
    run analytics. Commands to run this commands=["analytics"]
    """
    analytics.run(message, bot)

# handles predict command
@bot.message_handler(commands=["predict"])
def command_predict(message):
    """
    command_predict(message): Take an argument message with content and chat ID. Calls predict to 
    analyze budget and spending trends and suggest a future budget. Commands to run this commands=["predict"]
    """
    predict.run(message, bot)

def main():
    """
    main() The entire bot's execution begins here. It ensure the bot variable begins
    polling and actively listening for requests from telegram.
    """
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")

if __name__ == "__main__":
    main()
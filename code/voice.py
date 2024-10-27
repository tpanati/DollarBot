import os
import speech_recognition as sr
import tempfile
import add
import history
import predict
import monthly
import weekly
import budget
import helper
from pydub import AudioSegment
from telebot import types


def run(message, bot):
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
            process_command(text, message, bot)
        except sr.UnknownValueError:
            bot.reply_to(message, "Sorry, I could not understand the audio.")
        except sr.RequestError :
            bot.reply_to(message, "Could not request results from the speech recognition service.")

    # Cleanup: remove the temporary files
    os.remove(temp_ogg_path)
    os.remove(temp_wav_path)


def process_command(text, message, bot):
    if "expense" in text:
        add.run(message, bot)
    elif "history" in text:
        history.run(message, bot)  # Call the existing history command
    elif "budget" in text:
        budget.run(message, bot)  # Call the existing budget command
    elif "weekly" in text:
        weekly.run(message, bot)
    elif "monthly" in text:
        monthly.run(message, bot)
    elif "predict" in text:
        predict.run(message, bot)
    elif "help" in text:
        show_help(message, bot)
    elif "menu" or "start" in text:
        start_and_menu_command(message, bot)
    else:
        bot.send_message(message.chat.id, "I didn't recognize that command.")
        
def show_help(m, bot):
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

def start_and_menu_command(m, bot):
    helper.read_json()
    chat_id = m.chat.id
    text_intro = (
        "*Welcome to the Dollar Bot!* \n"
        "DollarBot can track all your expenses with simple and easy-to-use commands :) \n"
        "Here is the complete menu:\n\n"
    )

    commands = helper.getCommands()
    keyboard = types.InlineKeyboardMarkup()

    for command, _ in commands.items():  # Unpack the tuple to get the command name
        button_text = f"/{command}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=command))  # Use `command` as a string

    text_intro += "_Click a command button to use it._"
    bot.send_message(chat_id, text_intro, reply_markup=keyboard, parse_mode='Markdown')
    return True
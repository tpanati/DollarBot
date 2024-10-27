import os
import code.code as code
import speech_recognition as sr
import tempfile
from pydub import AudioSegment


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
        code.command_add(message)
    elif "history" in text:
        code.command_history(message)  # Call the existing history command
    elif "budget" in text:
        code.command_budget(message)  # Call the existing budget command
    elif "menu" in text:
        code.start_and_menu_command(message)
    elif "help" in text:
        code.show_help(message)
    elif "weekly" in text:
        code.command_weekly(message)
    elif "monthly" in text:
        code.command_monthly(message)
    elif "predict" in text:
        code.command_predict(message)
    else:
        bot.send_message(message.chat.id, "I didn't recognize that command.")
        

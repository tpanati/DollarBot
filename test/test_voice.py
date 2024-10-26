import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from code import handle_voice, process_command

class TestVoiceHandler(unittest.TestCase):
    
    @patch('bot.get_file')
    @patch('bot.download_file')
    @patch('tempfile.NamedTemporaryFile')
    @patch('pydub.AudioSegment.from_ogg')
    @patch('speech_recognition.Recognizer')
    def test_handle_voice_success(self, MockRecognizer, MockAudioSegment, MockNamedTempFile, MockDownloadFile, MockGetFile):
        # Mock file details and download
        MockGetFile.return_value.file_path = 'fake_path.ogg'
        MockDownloadFile.return_value = b'fake_ogg_data'
        
        # Mock tempfile behavior
        temp_ogg = MagicMock()
        temp_wav = MagicMock()
        MockNamedTempFile.side_effect = [temp_ogg, temp_wav]
        temp_ogg.name = 'temp.ogg'
        temp_wav.name = 'temp.wav'
        
        # Mock audio conversion
        MockAudioSegment.from_ogg.return_value.export = MagicMock()
        
        # Mock speech recognition
        recognizer_instance = MockRecognizer.return_value
        recognizer_instance.record.return_value = "fake_audio_data"
        recognizer_instance.recognize_google.return_value = "this is a test expense"
        
        # Mock process_command function
        with patch('process_command') as mock_process_command:
            handle_voice(MagicMock())  # Simulate calling the voice handler

            # Assertions
            MockGetFile.assert_called_once()
            MockDownloadFile.assert_called_once()
            MockAudioSegment.from_ogg.assert_called_once_with('temp.ogg')
            recognizer_instance.recognize_google.assert_called_once()
            mock_process_command.assert_called_once_with("this is a test expense", MagicMock())
        
        # Cleanup mocks
        os.remove('temp.ogg')
        os.remove('temp.wav')

    @patch('bot.send_message')
    def test_process_command(self, mock_send_message):
        message = MagicMock()
        
        # Test different commands
        with patch('command_add') as mock_command_add, \
             patch('command_history') as mock_command_history, \
             patch('command_budget') as mock_command_budget:
            
            process_command("add expense", message)
            mock_command_add.assert_called_once_with(message)
            
            process_command("show history", message)
            mock_command_history.assert_called_once_with(message)
            
            process_command("set budget", message)
            mock_command_budget.assert_called_once_with(message)
            
            # Test unrecognized command
            process_command("unknown command", message)
            mock_send_message.assert_called_once_with(message.chat.id, "I didn't recognize that command.")

if __name__ == '__main__':
    unittest.main()

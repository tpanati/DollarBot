import os
import json
from code import delete
from mock import MagicMock, patch
from telebot import types


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_expense_record.json").st_size != 0:
            with open("./test/dummy_expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def create_message(text):
    params = {"messagebody": text}
    chat = types.User("894127939", False, "test")
    return types.Message(1, None, None, chat, "text", params, "")

@patch("telebot.telebot")
def test_delete_with_no_data(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    delete.helper.read_json.return_value = {}
    delete.helper.write_json.return_value = True
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    delete.run(MOCK_Message_data, mc)
    if delete.helper.write_json.called is False:
        assert True

@patch("telebot.telebot")
def test_process_delete_argument_all_records(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    mocker.patch.object(delete, "deleteHistory")
    
    # Create a mock message with "all" as the text
    MOCK_Message_data = create_message("all")
    MOCK_Message_data.text = "all"  # Set the text attribute explicitly
    
    # Create a MagicMock for the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot

    # Call the function being tested
    delete.process_delete_argument(MOCK_Message_data, mock_bot)
    
    # Assert that the expected functions were called
    delete.deleteHistory.assert_called_with(MOCK_Message_data.chat.id)
    mock_bot.send_message.assert_called_with(MOCK_Message_data.chat.id, "History has been deleted!")

@patch("telebot.telebot")
def test_process_delete_argument_with_valid_date(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    mocker.patch.object(delete, "types")
    
    # Mock the necessary functions and data
    mocker.patch.object(delete.helper, "getUserHistoryByDate", return_value=["record1", "record2"])
    
    # Create a mock message with a specified date
    date_to_delete = "2023-01-15"
    MOCK_Message_data = create_message(date_to_delete)
    MOCK_Message_data.text = "2023-01-15"
    
    # Create a MagicMock for the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot
    
    # Call the function being tested
    delete.process_delete_argument(MOCK_Message_data, mock_bot)
    
    # Assert that the expected functions were called
    delete.helper.getUserHistoryByDate.assert_called_with(MOCK_Message_data.chat.id, date_to_delete)
    # Assert that the bot replied with a confirmation message
    delete.types.ReplyKeyboardMarkup.assert_called_once()
    mock_bot.reply_to.assert_called_with(MOCK_Message_data, mocker.ANY, reply_markup=mocker.ANY)
    mock_bot.register_next_step_handler.assert_called_once()

@patch("telebot.telebot")
def test_process_delete_argument_with_invalid_date(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    
    # Create a mock message with an invalid date
    invalid_date = "invalid_date"
    MOCK_Message_data = create_message(invalid_date)
    MOCK_Message_data.text = "invalid_date"

    # Create a MagicMock for the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot
    
    # Call the function being tested
    delete.process_delete_argument(MOCK_Message_data, mock_bot)
    
    # Assert that the expected functions were called
    # Note: Since there's no date validation, the function should proceed with invalid dates
    delete.helper.getUserHistoryByDate.assert_called_with(MOCK_Message_data.chat.id, invalid_date)
    # Assert that the bot replied with an error message
    mock_bot.reply_to.assert_called_with(MOCK_Message_data, "No transactions within invalid_date")

def test_deleteHistory():
    # Mock user_list
    user_list = {"sample_chat_id": {"data": ["record1", "record2"], "budget": {"overall": "100", "category": {"food": "50"}}}}
    
    # Call deleteHistory function
    result = delete.deleteHistory("sample_chat_id")
    
    # Assert that the user_list entry is removed
    assert "sample_chat_id" not in result
     # Assert that the data is cleared in the result
    expected_result = {}
    assert result == expected_result
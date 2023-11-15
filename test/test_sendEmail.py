import pytest
from unittest.mock import patch, MagicMock
from code import sendEmail

@pytest.fixture
def bot():
    return MagicMock()

@pytest.fixture
def message():
    return MagicMock()

@patch("sendEmail.helper")
@patch("sendEmail.logging")
def test_run_with_valid_user(mock_logging, mock_helper, message, bot):
    mock_helper.read_json.return_value = {"sample_chat_id": {"data": ["record1,food,50", "record2,entertainment,30"]}}

    sendEmail.run(message, bot)

    mock_helper.read_json.assert_called_once()
    mock_helper.getUserHistory.assert_called_once_with("sample_chat_id")
    bot.send_message.assert_called_with(message.chat.id, "Enter your email id")

@patch("sendEmail.helper")
@patch("sendEmail.logging")
@patch("sendEmail.csv")
@patch("sendEmail.smtplib")
@patch("sendEmail.MIMEMultipart")
@patch("sendEmail.MIMEText")
@patch("sendEmail.MIMEBase")
@patch("sendEmail.encoders")
@patch("sendEmail.open")
def test_acceptEmailId_with_valid_email(mock_open, mock_encoders, mock_MIMEBase,
                                        mock_MIMEText, mock_MIMEMultipart, mock_smtplib,
                                        mock_csv, mock_logging, mock_helper, message, bot):
    message.text = "valid@example.com"
    mock_helper.getUserHistory.return_value = ["record1,food,50", "record2,entertainment,30"]

    with patch("builtins.open", mock_open):
        sendEmail.acceptEmailId(message, bot)

    bot.send_message.assert_called_once_with(message.chat.id, "Mail Sent")

@patch("sendEmail.helper")
@patch("sendEmail.logging")
def test_acceptEmailId_with_invalid_email(mock_logging, mock_helper, message, bot):
    message.text = "invalid_email"
    sendEmail.acceptEmailId(message, bot)

    bot.send_message.assert_called_once_with(message.chat.id, 'incorrect email')

# Add more test cases as needed

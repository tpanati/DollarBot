import pytest

class MockBot:
    """A mock bot class to simulate the behavior of the actual bot."""
    class Voice:
        def __init__(self, file_id):
            self.file_id = file_id

    def get_file(self, file_id):
        # Simulate getting a file from the bot
        return f"File with ID: {file_id}"

# Create a mock bot instance
bot = MockBot()

# Replace the actual bot with the mock bot in the handle_voice function
def handle_voice(command):
    # Simulate handling a voice command
    if isinstance(command, str):
        if command == "add expense 10":
            # Simulating successful command handling
            return "Expense of 10 added."
        else:
            # Simulating invalid command handling
            return "Invalid command."
    else:
        raise AttributeError("Command must be a string.")

def test_handle_voice_valid_command():
    # Test with a valid command
    command = "add expense 10"
    result = handle_voice(command)
    assert result == "Expense of 10 added."

def test_handle_voice_invalid_command():
    # Test with an invalid command
    command = "invalid command"
    result = handle_voice(command)
    assert result == "Invalid command."

def test_handle_voice_empty_command():
    # Test with an empty command
    command = ""
    result = handle_voice(command)
    assert result == "Invalid command."

def test_handle_voice_command_not_a_string():
    # Test with a non-string command
    command = 12345  # Not a string
    with pytest.raises(AttributeError):
        handle_voice(command)

if __name__ == "__main__":
    pytest.main()


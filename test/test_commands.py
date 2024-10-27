import pytest
from voice import process_command
from code.exception import InvalidOperationError

# Example implementation of the process_command function (replace with your actual logic)
def process_command(command):
    if command == "get balance":
        return "Your current balance is $100."
    elif command == "add expense 10":
        return "Expense of 10 added."
    elif command.startswith("remove expense"):
        # Example of removing expense
        return "Expense removed."
    else:
        raise InvalidOperationError("Invalid operation.")

# Test cases for process_command
def test_process_command_valid_get_balance():
    command = "get balance"
    result = process_command(command)
    assert result == "Your current balance is $100."

def test_process_command_valid_add_expense():
    command = "add expense 10"
    result = process_command(command)
    assert result == "Expense of 10 added."

def test_process_command_valid_remove_expense():
    command = "remove expense 10"
    result = process_command(command)
    assert result == "Expense removed."

def test_process_command_invalid_command():
    command = "invalid command"
    with pytest.raises(InvalidOperationError, match="Invalid operation."):
        process_command(command)

def test_process_command_empty_command():
    command = ""
    with pytest.raises(InvalidOperationError, match="Invalid operation."):
        process_command(command)


if __name__ == "__main__":
    pytest.main()

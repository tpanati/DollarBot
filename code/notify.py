from jproperties import Properties
from notifier import TelegramNotifier

configs = Properties()

def notify(chat_id, cat, amount):
    """
    Sends a notification to a Telegram chat about a budget exceeding.

    Parameters:
    - chat_id (str): The chat ID where the notification will be sent.
    - cat (str): The category for which the budget exceeded.
    - amount (str): The amount by which the budget exceeded.

    This function reads the Telegram API token from a configuration file,
    creates a TelegramNotifier object, and sends a notification to the specified
    chat ID about the budget exceeding for the given category and amount.
    """

    print("inside notify")
    with open("user.properties", "rb") as read_prop:
        configs.load(read_prop)
    token = str(configs.get("api_token").data)
    print(token)
    notifier = TelegramNotifier(token, parse_mode="HTML", chat_id=chat_id)
    msg = "<b>Budget for " + cat + " exceeded by $" + amount + " !!!!</b>"
    notifier.send(msg)
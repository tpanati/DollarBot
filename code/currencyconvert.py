# currency_converter.py

from forex_python.converter import CurrencyRates
from datetime import datetime
import helper

# Initialize CurrencyRates object
c = CurrencyRates()

# Fallback rates in case the API is unreachable
DOLLARS_TO_POUNDS = 0.78
DOLLARS_TO_CANADIAN_DOLLAR = 1.34
DOLLARS_TO_RUPEES = 84
DOLLARS_TO_EUROS = 0.95
DOLLARS_TO_SWISS_FRANC = 0.9

# Fetch real-time rates or fallback to defaults
def get_conversion_rate(currency_code):
    try:
        if currency_code == 'INR':
            return c.get_rate('USD', 'INR')
        elif currency_code == 'EUR':
            return c.get_rate('USD', 'EUR')
        elif currency_code == 'CHF':
            return c.get_rate('USD', 'CHF')
        elif currency_code == 'GBP':
            return c.get_rate('USD', 'GBP')
        elif currency_code == 'CAD':
            return c.get_rate('USD', 'CAD')
    except:
        # Fallback rates
        if currency_code == 'INR':
            return DOLLARS_TO_RUPEES
        elif currency_code == 'EUR':
            return DOLLARS_TO_EUROS
        elif currency_code == 'CHF':
            return DOLLARS_TO_SWISS_FRANC
        elif currency_code == 'GBP':
            return DOLLARS_TO_POUNDS
        elif currency_code == 'CAD':
            return DOLLARS_TO_CANADIAN_DOLLAR
    return 1

def get_latest_spendings():
    # Retrieve stored spendings data from JSON using helper
    spendings = helper.read_json()
    if not spendings:
        return []

    # Flatten the records into a list for easier processing
    all_spendings = []
    for user_data in spendings.values():
        all_spendings.extend(user_data.get("data", []))
    print("Retrieved spendings:", all_spendings)      #Debug output
    return all_spendings

def calculate_spendings_in_currency( currency_code):
    # Calculate spendings and convert them
    query_results = get_latest_spendings()
    print("Query results:", query_results)
    total_dict = {}
    rate = get_conversion_rate(currency_code)
    print(f"Conversion rate for {currency_code}: {rate}")

    for row in query_results:
        # date, category, money
        if row.count(',') == 2:
            s = row.split(',')
            category = s[1]
            amount = float(s[2])
        else:
            print(f"Skipping malformed entry: {row}")
        # Aggregate amounts per category
        total_dict[category] = total_dict.get(category, 0) + amount
        

    # Format spending summary in the chosen currency
    total_text = ""
    for category, amount in total_dict.items():
        converted_amount = round(amount * rate, 2)
        currency_symbol = get_currency_symbol(currency_code)
        total_text += f"{category} {currency_symbol}{converted_amount}\n"
    print(f"Conversion rate for {currency_code}: {rate}")
    print(f"Total dictionary of spendings: {total_dict}")

    return total_text if total_text else "No converted spendings available."

def get_currency_symbol(currency_code):
    return {
        'INR': '₹',
        'EUR': '€',
        'CHF': '₣',
        'GBP': '£',
        'CAD': 'C$'
    }.get(currency_code, '$')

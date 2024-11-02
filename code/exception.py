class InvalidAmountError(Exception):
    """Exception raised for invalid amounts."""
    def __init__(self, message="Invalid amount."):
        super().__init__(message)
    
class InvalidDurationError(Exception):
    """Exception raised for invalid duration."""
    def __init__(self, message="Invalid duration."):
        super().__init__(message)

class InvalidCategoryError(Exception):
    """Exception raised for invalid categories."""
    def __init__(self, category, message="Invalid category selected"):
        self.category = category
        self.message = message
        super().__init__(f'{message}: "{category}"')

class InvalidOperationError(Exception):
    """Exception raised for invalid operations."""
    def __init__(self, operation, message="Invalid operation selected"):
        self.operation = operation
        self.message = message
        super().__init__(f'{message}: "{operation}"')

class BudgetError(Exception):
    """Exception raised for invalid budget operations."""
    def __init__(self, message="Invalid budget."):
        super().__init__(message)

class DisplayOptionError(Exception):
    """Exception raised for invalid spending display options."""
    def __init__(self, message="Invalid display option."):
        super().__init__(message)

class NoHistoryError(Exception):
    """Exception raised when a user has no spending history."""
    def __init__(self, message="No spending records found."):
        super().__init__(message)
    
class NoSpendingRecordsError(Exception):
    """Exception raised when there are no spending records for the user."""
    def __init__(self, message="Sorry! No spending records found."):
        super().__init__(message)

class EstimateNotAvailableError(Exception):
    """Exception raised when an estimate is not available for a given category."""
    def __init__(self, day_week_month):
        message = f'Sorry, I can\'t show an estimate for "{day_week_month}"!'
        super().__init__(message)

class BudgetNotFoundError(Exception):
    """Exception raised when a budget does not exist."""
    def __init__(self, message):
        super().__init__(message)

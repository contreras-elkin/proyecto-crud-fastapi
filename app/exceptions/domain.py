
class DomainError(Exception):
    pass

class UserNotFoundError(DomainError):
    def __init__(self, user_id):
        self.user_id=user_id
        super().__init__(f"User not found")
        
class ExpenseNotFoundError(DomainError):
    def __init__(self, expense_id):
        self.expense_id=expense_id
        super().__init__(f"Expense not found")

class UserEmailExists(DomainError):
    def __init__(self, email):
        self.email=email
        super().__init__(f"Email already existis")

class UserNameExists(DomainError):
    def __init__(self, user_name):
        self.user_name=user_name
        super().__init__(f"user_name already existis")

class UserPhoneExists(DomainError):
    def __init__(self, phone):
        self.phone= phone
        super().__init__(f"Phone already exists")

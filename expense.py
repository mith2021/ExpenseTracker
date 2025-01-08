class Expense:
    #defining what an expense is (Expense Data Type)
    def __init__(self, name, amount, category, is_recurring ) -> None:
        #attributes are being assigned to what is being passed into the
        # init function
        # the expense's name is going be to be the name that we pass in
        self.name = name
        self.amount = float(amount)
        self.category = category
        self.is_recurring = is_recurring
    def edit_name(self, new_name):
        self.name = new_name
    
    def edit_amount(self, amount):
        self.name = amount

    def edit_category(self, category):
        self.name = category

    def edit_is_recurring(self, recurring):
        self.name = recurring

    def __str__(self):
        return (f"Name: {self.name} Amount: {self.amount} Category: {self.category} Recurring: {self.is_recurring} \n")


expense_list = []

test_exp1 = Expense("Shein", "146.8", "clothing", "no")
test_exp2 = Expense("Starbucks Coffee", "5.75", "Food", False)
test_exp3 = Expense("Netflix Subscription", "15.99", "Entertainment", True)
test_exp4 = Expense("Monthly Rent", "1200.00", "Housing", True)
expense_list.append(test_exp1)
expense_list.append(test_exp2)
expense_list.append(test_exp3)
expense_list.append(test_exp4)



def check_to_escape(prompt):
    user_input =  prompt
    if user_input == 'q':
        mainScreen()
    else:
        return user_input
    
def mainScreen():
    global income 
    menu_options = ["Add Expense", "View Expenses", "Remove an Expense", "Edit Expense"]
    for index, option in enumerate(menu_options, 1):
        print(f"{index}. {option}") 
    choice = check_to_escape(input("What would you like to do?  \n"))
    if choice.isdigit:
        return int(choice)
    elif choice == 'q':
        return choice
    else:
        print("Please provide a valid input\n")
        mainScreen()
    
def create_expense():
    while True:
        print("Please provide the following information:")
        ex = Expense(check_to_escape(input("Name: ")),
                     check_to_escape(input("Amount: ")),
                     check_to_escape(input("Category: ")),
                     check_to_escape(input("Reccuring: ")))
        expense_list.append(ex)
        if input("Would you like to add another expense? (y/n) ") == 'n':
            break

def display_expenses():
    global income
    
    if not getattr(display_expenses, 'asked', False):
        income = float(input("What is your monthly income? "))
        display_expenses.asked = True
        
    total_amt = 0
    print('\n' + '*'*50)
    for expense in expense_list:
        print(expense)
        total_amt += expense.amount
    print(f"Your Total Expenses: {total_amt}" )

    discretionary_income = income - total_amt
    print(f'Your monthly income is: {income}')
    print(f"You have {discretionary_income} left over this month" + '\n' + '*'*50 + '\n')

def display_only_expenses():
    for num, expense in enumerate(expense_list, 1):
        print(f"{num}. Name: {expense.name} Amount: {expense.amount} Category: {expense.category} Is recurring: {expense.is_recurring}")


#start using enumerate to get indexes as well
def remove_expense():
    display_only_expenses()
    try:
        remove = int(check_to_escape(input('Which expense would you like to remove? (num) '))) - 1
        if 0 <= remove < len(expense_list):
            expense_list.pop(remove)
            print("Expense removed successfully.")
        else:
            print("Invalid number. Please try again.")
    except ValueError:
        print("Please provide a valid number.")

def edit_expense(): 
    if not expense_list:
        print("No expenses available to edit.")
        return 
    
    display_only_expenses()

    try:
        edit = int(check_to_escape(input('Which expense would you like to change? (num) '))) - 1
        print('')
        if edit < 1 or edit > len(expense_list):
            print('Invalid choice. Returning to the menu.')
            return
        
        editing_expense = expense_list[edit]
        print(editing_expense)
        
        print("You can change the following attributes: name, amount, category, recurring")
        edit_attr = check_to_escape(input("What would you like to change? (Enter the attribute name): ")).strip().lower()

        if edit_attr == 'name':
            editing_expense.edit_name(check_to_escape(input(f'what should the new name be?  (Current: {edit_attr.name})')).strip())

        elif edit_attr == "amount":
            new_amount = check_to_escape(input(f"Enter a new amount (current: ${editing_expense.amount}): ")).strip()
            try:
                editing_expense.amount = float(new_amount)
                print("Amount updated successfully!")
            except ValueError:
                print("Invalid amount. Keeping the current value.")
        
        elif edit_attr == 'category':
            new_category = check_to_escape(input(f"Enter a new category (current: ${editing_expense.category}): ")).strip()
            editing_expense.category = new_category
        elif edit_attr == 'recurring':
            is_recurring = input(f'Is this expense recurring? (currently {editing_expense.is_recurring}) (Yes/No): ')
            try:
                if is_recurring == 'Yes':
                    editing_expense.is_recurring = True
                elif is_recurring == 'No':
                    editing_expense.is_recurring = False
            except:
                print('Please provide a valid response.')
                
    except ValueError:
        print("Please provide a valid number.")

print("Welcome to Expense Tracker!")

while True:
    try:
        choice = mainScreen()
        if choice == 'q':
            SystemExit('Exiting Expense Tracker...')
        elif choice == 1:
            create_expense()
        elif choice == 2:
            display_expenses()
        elif choice == 3:
            remove_expense()
        elif choice == 4:
            edit_expense()
    except ValueError:
        print("Invalid choice. Please try again.\n")

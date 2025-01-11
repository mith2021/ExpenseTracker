import sys
import csv
import os

# Classes
class Expense:
    #defining what an expense is (Expense Data Type)
    def __init__(self, name, amount, category, is_recurring=False ) -> None:
        #attributes are being assigned to what is being passed into the
        # init function
        # the expense's name is going be to be the name that we pass in
        self.name = name
        self.amount = float(amount)
        self.category = category
        self.is_recurring = is_recurring

    def __str__(self):
        return (f"Name: {self.name} Amount: {self.amount} Category: {self.category} Recurring: {self.is_recurring} \n")

expense_list = []
#Test cases
test_exp1 = Expense("Shein", "146.8", "clothing", "no")
test_exp2 = Expense("Starbucks Coffee", "5.75", "Food", False)
test_exp3 = Expense("Netflix Subscription", "15.99", "Entertainment", True)
test_exp4 = Expense("Monthly Rent", "1200.00", "Housing", True)
expense_list.append(test_exp1)
expense_list.append(test_exp2)
expense_list.append(test_exp3)
expense_list.append(test_exp4)



#------------------Helper Functions------------------

def check_to_escape(prompt):
    if prompt.lower() == 'q':
        mainScreen()  # Redirect to main menu
        # Explicitly return a recognizable value
    else:
        return prompt

def create_spend_chart(categories, income):
    categories_list = [ex.category for ex in expense_list]
    spends = {}
    for category in categories_list:
        spends[category] = 0
        for ex in expense_list:
            if ex.category == category:
                spends[category] += ex.amount
    
    percentages = [(spend / income) * 100 for spend in spends.values()]

    chart = 'Percentage spent by category\n'

    for i in range(100, -1, -10):
        line = f"{i:>3}| "
        for percent in percentages:
            if percent >= i:
                line += "o  "
            else:
                line += "   "
        chart += line + "\n"

    chart += "    " + "---" * len(categories) + "-\n"

    max_length = max([len(category) for category in categories_list])
    names = [category.ljust(max_length) for category in categories_list]
    for i in range(max_length):
        line = '     '
        for name in names:
            line += name[i] + '  '
        chart += line.rstrip() + '\n'
    return chart


#------------------Main Program Functions------------------
def mainScreen():
    global income 
    menu_options = ["Add Expense", "View Expenses", "Remove an Expense", "Edit Expense"]
    for index, option in enumerate(menu_options, 1):
        print(f"{index}. {option}") 
    print("Press q to quit at any time during the program")
    choice = input("What would you like to do?  ")
    if choice == 'q':
        sys.exit('Exiting Expense Tracker...')
    elif choice.isdigit():
        return int(choice)
    
def create_expense():
    while True:
        print("Please provide the following information:")
        ex = Expense(check_to_escape(input("Name: ")),
                     check_to_escape(input("Amount: ")),
                     check_to_escape(input("Category: ")),
                    )
        try:
            if check_to_escape(input("Recurring? (y/n) ")) == 'y': 
                ex.is_recurring = True
            else:
                ex.is_recurring = False
        except ValueError:
            print("Please provide a valid input")   
        expense_list.append(ex)
        if check_to_escape(input("Would you like to add another expense? (y/n) ")) == 'n':
            break

def view_expenses():
    global income
    
    if not getattr(view_expenses, 'asked', False):
        income = float(check_to_escape(input("What is your monthly income? ")))
        view_expenses.asked = True
        
    total_amt = 0
    print('\n' + '*'*50)
    for expense in expense_list:
        print(expense)
        total_amt += expense.amount
    print(f"Your Total Expenses: {total_amt}" )

    discretionary_income = income - total_amt
    print(f'Your monthly income is: {income}')
    print(f"You have ${discretionary_income:.2f} left over this month" + '\n' + '*'*50 + '\n')
    
    chart_question = input('Would you like to see a chart of your expenses?(y/n)  ')
    if chart_question.lower() == 'y':
        print(create_spend_chart(expense_list, income))


def display_only_expenses():
    for num, expense in enumerate(expense_list, 1):
        print(f"{num}. Name: {expense.name} Amount: {expense.amount} Category: {expense.category} Is recurring: {expense.is_recurring}")


#start using enumerate to get indexes as well
def remove_expense():
    if not expense_list: 
        print("No expenses available to remove.")
        mainScreen()

    display_only_expenses()
    num = check_to_escape(input("Which expense would you like to remove? (num):  "))
    try:
        if 0 < int(num) < len(expense_list):
            index = int(num) - 1 
            expense_list.pop(index)
            print(f"Expense {expense_list[index].name} has been removed.")
        else:
            print("Invalid choice. Please try again.")    
    except ValueError:
        print("Invalid input. Please enter a number.")
def edit_expense(): 
    if not expense_list:
        print("No expenses available to edit.")
        return 
    
    display_only_expenses()

    try:
        edit = int(check_to_escape(input('Which expense would you like to change? (num) '))) - 1
        print('')
        if edit < 0 or edit > len(expense_list):
            print('Invalid choice. Returning to the menu.')
            return
        
        editing_expense = expense_list[edit]
        print(editing_expense)
        
        print("You can change the following attributes: name, amount, category, recurring")
        edit_attr = check_to_escape(input("What would you like to change? (Enter the attribute name): ")).strip().lower()
        try:
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
                is_recurring = check_to_escape(input(f'Is this expense recurring? (currently {editing_expense.is_recurring}) (Yes/No): '))
                try:
                    if is_recurring.lower() == 'yes':
                        editing_expense.is_recurring = True
                    elif is_recurring.lower() == 'no':
                        editing_expense.is_recurring = False
                except:
                    print('Please provide a valid response.')
        except:
            print('Please provide a valid response.')
    except ValueError:
        print("Please provide a valid number.")




#----------------Program Loop------------------
print("Welcome to Expense Tracker!")

while True:
    try:
        choice = mainScreen()
        if choice == 1:
            create_expense()
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            remove_expense()
        elif choice == 4:
            edit_expense()
    except ValueError:
        print("Invalid choice. Please try again.\n")

import random
from colorama import Fore, Style, init

init(autoreset=True)

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 1000

ROWS = 3
COLS = 3

symbols_count = {
    '🍒': 2,
    '🍋': 4,
    '🍊': 6,
    '🍇': 8,
    '🔔': 3,
    '🍫': 5,
}

symbols_values = {
    '🍊': 5,
    '🍇': 4,
    '🍋': 3,
    '🍒': 2,
    '🔔': 6,
    '🍫': 1,
}

def check_winning(columns, lines, bet, symbols_values):
    winning = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol_to_check != symbol:
                break
        else:
            winning += symbols_values[symbol] * bet
            winning_lines.append(line + 1)
            
    return winning, winning_lines

def get_slot_machine_spin(rows, cols, symbols_count):
    all_symbols = []
    for symbol, symbol_count in symbols_count.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
            
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)
            
    return columns
    
def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for col in range(len(columns)):
            print(Fore.YELLOW + f"| {columns[col][row]} ", end="")
        print(Fore.YELLOW + "|")

def deposit():
    while True:
        amount = input(Fore.CYAN + "Enter the amount you want to deposit? Rs. ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print(Fore.RED + "Amount must be greater than 0.")
        else:
            print(Fore.RED + "Please enter a valid amount.")
        
    return amount

def get_no_of_lines():
    while True:
        lines = input(Fore.CYAN + f"Enter the number of lines you want to BET on (1-{MAX_LINES})? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(Fore.RED + f"Number of lines must be between 1 and {MAX_LINES}.")
        else:
            print(Fore.RED + "Please enter a valid number of lines.")
        
    return lines

def get_bet_amount(balance):
    while True:
        bet = input(Fore.CYAN + "Enter the amount you want to bet? Rs. ")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                if bet <= balance:
                    break
                else:
                    print(Fore.RED + "You don't have enough balance.")
            else:
                print(Fore.RED + f"Bet amount must be between Rs.{MIN_BET} and Rs.{MAX_BET}.")
        else:
            print(Fore.RED + "Please enter a valid bet amount.")
    return bet

def play_game(balance):
    while True:
        lines = get_no_of_lines()
        while True:
            bet = get_bet_amount(balance)
            total_bet = bet * lines

            if total_bet > balance:
                print(Fore.RED + f"You don't have enough balance to bet that much. Your current balance is Rs.{balance}. Please try again.")
            else:
                break
        
        print(Fore.GREEN + f"You are betting Rs.{bet} on {lines} lines. Total bet is Rs.{total_bet}.")
        print(Fore.GREEN + "Good Luck!!")

        slots = get_slot_machine_spin(ROWS, COLS, symbols_count)
        print_slot_machine(slots)
        winnings, winning_lines = check_winning(slots, lines, bet, symbols_values)
        print(Fore.GREEN + f"YOU WON Rs.{winnings}.")
        if winning_lines:
            print(Fore.GREEN + "YOU WON on lines", *winning_lines)
        else:
            print(Fore.RED + "You didn't win on any lines.")

        balance += winnings - total_bet
        print(Fore.CYAN + f"Your current balance is Rs.{balance}.")

        if balance <= 0:
            print(Fore.RED + "You have run out of balance. Game over!")
            break

        play_again = input(Fore.CYAN + "Do you want to play again? (Y/N): ").lower()
        if play_again not in ['y', 'yes']:
            print(Fore.GREEN + "Thank you for playing! Goodbye!")
            break
    
    return balance

def main():
    print(Fore.GREEN + "Welcome to the Slot Machine Game!!")
    balance = deposit()
    final_balance = play_game(balance)
    print(Fore.YELLOW + f"Your final balance is Rs.{final_balance}.")
    
main()

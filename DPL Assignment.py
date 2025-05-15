import os
import time
import datetime

# ------------------- Utility Functions -------------------
def string_length(s):
    count = 0
    while True:
        try:
            s[count]
            count += 1
        except IndexError:
            break
    return count

def remove_newline(s):
    result = ''
    i = 0
    while True:
        try:
            if s[i] == '\n':
                break
            result += s[i]
            i += 1
        except IndexError:
            break
    return result

def manual_parse_line(line):
    line = remove_newline(line)
    i = 0
    while i < string_length(line) and line[i] != ' ':
        i += 1
    if i == string_length(line):
        return None, None
    saved_username = line[:i]
    saved_password = line[i+1:]
    return saved_username, saved_password

def compare_strings(str1, str2):
    i = 0
    while i < string_length(str1) and i < string_length(str2):
        if str1[i] != str2[i]:
            return False
        i += 1
    return i == string_length(str1) and i == string_length(str2)

# ------------------- Authentication -------------------
def register():
    os.system('cls')
    newusername = input("Enter your new username : ")
    newpassword = input("Enter your new password : ")
    comfirmpassword = input("Confirm password        : ")

    while newpassword != comfirmpassword:
        print("New Passwords do not match. Try again.")
        comfirmpassword = input("Confirm password        : ")

    try:
        with open("Register.txt", "r") as file:
            for line in file:
                saved_username, _ = manual_parse_line(line)
                if saved_username and compare_strings(saved_username, newusername):
                    print("Username already exists. Returning to menu.")
                    time.sleep(2)
                    return False
    except FileNotFoundError:
        pass

    with open("Register.txt", "a") as file:
        file.write(newusername + " " + newpassword + "\n")

    with open("current_user.txt", "w") as f:
        f.write(newusername)

    print("Successfully Registered.")
    time.sleep(2)
    return True

def login():
    attempts = 4
    while attempts > 0:
        os.system('cls')
        username = input("Enter your username : ")
        password = input("Enter your password : ")

        found = False
        try:
            with open("Register.txt", "r") as file:
                for line in file:
                    saved_username, saved_password = manual_parse_line(line)
                    if saved_username and compare_strings(saved_username, username) and compare_strings(saved_password, password):
                        found = True
                        break
        except FileNotFoundError:
            print("No registered users found.")
            return False

        if found:
            with open("current_user.txt", "w") as f:
                f.write(username)
            print("Login Successful")
            time.sleep(2)
            return True
        else:
            attempts -= 1
            print(f"Invalid credentials. Attempts left: {attempts}")
            time.sleep(2)
    return False

# ------------------- Booking -------------------
def get_current_user():
    try:
        with open("current_user.txt", "r") as f:
            return remove_newline(f.readline())
    except FileNotFoundError:
        return ""

def book_table():
    tables = ["T1", "T2", "T3", "T4"]
    print("------ TABLE BOOKING ------")
    name = input("Enter your name: ")
    date_str = input("Enter booking date (YYYY-MM-DD): ")
    time_str = input("Enter booking time (HH:MM, 24hr format): ")
    user = get_current_user()

    try:
        booking_datetime = datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        if booking_datetime < now:
            print("Booking time must be in the future.")
            return

        print("Available tables:")
        for t in tables:
            print("-", t)
        chosen_table = input("Choose a table (e.g., T1): ")

        if chosen_table not in tables:
            print("Invalid table choice.")
            return

        try:
            with open("booking.txt", "r") as f:
                for line in f:
                    record = line.strip().split(",")
                    if record[2] == date_str and record[3] == time_str and record[5] == chosen_table:
                        print("Table already booked.")
                        return
        except FileNotFoundError:
            pass

        customers = int(input("Enter number of people (max 6): "))
        if customers <= 0 or customers > 6:
            print("Number of people must be between 1 and 6.")
            return

        with open("booking.txt", "a") as f:
            f.write(f"{user},{name},{date_str},{time_str},{customers},{chosen_table}\n")

        with open("current_booking.txt", "w") as f:
            f.write(f"{user},{name},{date_str},{time_str},{customers},{chosen_table}")

        print("Booking successful!")

    except ValueError:
        print("Invalid date/time format.")

# ------------------- Ordering -------------------
def load_menu():
    items = []
    try:
        with open("menu.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                items.append((parts[0], float(parts[1])))
    except FileNotFoundError:
        print("Menu file not found.")
    return items

def place_order():
    print("------ FOOD ORDERING ------")
    menu = load_menu()
    if not menu:
        return

    user = get_current_user()
    try:
        with open("current_booking.txt", "r") as f:
            booking_info = f.readline().strip()
            if booking_info.split(",")[0] != user:
                print("No valid booking under your account.")
                return
    except FileNotFoundError:
        print("No current booking found. Please book a table first.")
        return

    total = 0
    order_details = []

    for i, item in enumerate(menu):
        print(f"{i + 1}. {item[0]} - RM{item[1]:.2f}")

    while True:
        try:
            choice = int(input("Enter item number to order (0 to finish): "))
            if choice == 0:
                break
            if not (1 <= choice <= len(menu)):
                print("Invalid item number.")
                continue

            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be at least 1.")
                continue

            selected_item = menu[choice - 1]
            order_details.append((selected_item[0], selected_item[1], qty))
            total += selected_item[1] * qty

        except ValueError:
            print("Invalid input.")

    with open("order.txt", "w") as f:
        for item in order_details:
            f.write(f"{booking_info},{item[0]},{item[1]},{item[2]}\n")

    with open("total.txt", "w") as f:
        f.write(f"{total:.2f}\n")

    print(f"Order recorded. Total: RM{total:.2f}")

# ------------------- Receipt & History -------------------
def generate_receipt():
    user = get_current_user()
    try:
        with open("order.txt", "r") as f:
            found = False
            print("------ RECEIPT ------")
            for line in f:
                parts = line.strip().split(",")
                if parts[0] != user:
                    continue
                name, date, time, _, table = parts[1:6]
                item, price, qty = parts[6], float(parts[7]), int(parts[8])
                print(f"Customer: {name} | Table: {table} | {item} x{qty} @ RM{price:.2f} = RM{price * qty:.2f}")
                found = True
        if found:
            with open("total.txt", "r") as f:
                total = f.read().strip()
                print(f"Total: RM{total}")
        else:
            print("No receipt found for this account.")
    except FileNotFoundError:
        print("No receipt found. Please order first.")

def display_records():
    user = get_current_user()
    try:
        print("------ HISTORICAL BOOKINGS ------")
        with open("booking.txt", "r") as f:
            for line in f:
                if line.startswith(user + ","):
                    print(line.strip())
    except FileNotFoundError:
        print("No historical records found.")

# ------------------- Main Program -------------------
def display_menu():
    print("------------------------------------------------------")
    print("                       WELCOME                        ")
    print("------------------------------------------------------")
    print("                   A. Register                        ")
    print("                   B. Log in                          ")
    print("------------------------------------------------------")
    return input("Enter your choice (A/B): ")

def display_main_menu():
    while True:
        print("--------------------------------------------------")
        print("     WELCOME TO RESTAURANT RESERVATION SYSTEM     ")
        print("--------------------------------------------------")
        print("                  1. Booking Seat                 ")
        print("                  2. Order Product                ")
        print("                  3. Historical Record            ")
        print("                  4. Edit Table Message           ")
        print("                  5. Payment                      ")
        print("                  6. Log Out                      ")
        print("--------------------------------------------------")
        try:
            choice = int(input("Please enter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

# ------------------- Entry Point -------------------
while True:
    os.system('cls')
    choice = display_menu()

    if choice.upper() == "A":
        if not register():
            continue
        if not login():
            continue
    elif choice.upper() == "B":
        if not login():
            continue
    else:
        print("Invalid choice. Try again.")
        continue

    while True:
        os.system('cls')
        choice1 = display_main_menu()

        if choice1 == 1:
            os.system('cls')
            book_table()
            input("Press Enter to continue...")
        elif choice1 == 2:
            os.system('cls')
            place_order()
            input("Press Enter to continue...")
        elif choice1 == 3:
            os.system('cls')
            display_records()
            input("Press Enter to continue...")
        elif choice1 == 4:
            print("Edit Table Message - Feature not implemented.")
            input("Press Enter to continue...")
        elif choice1 == 5:
            os.system('cls')
            generate_receipt()
            input("Press Enter to continue...")
        elif choice1 == 6:
            print("Logging out...")
            time.sleep(1)
            break

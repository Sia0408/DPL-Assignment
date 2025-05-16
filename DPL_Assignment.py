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
    return line[:i], line[i+1:]

def compare_strings(str1, str2):
    i = 0
    while i < string_length(str1) and i < string_length(str2):
        if str1[i] != str2[i]:
            return False
        i += 1
    return i == string_length(str1) and i == string_length(str2)

def get_current_user():
    try:
        with open("data.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith("CURRENT_USER:"):
                    return remove_newline(line[13:])
    except:
        pass
    return ""

def set_current_user(username):
    lines = []
    try:
        with open("data.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if not line.startswith("CURRENT_USER:"):
                    lines.append(line)
    except:
        pass
    with open("data.txt", "w") as f:
        for l in lines:
            f.write(l)
        f.write("CURRENT_USER:" + username + "\n")

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
        with open("data.txt", "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                if line.startswith("USER:"):
                    saved_username, _ = manual_parse_line(line[5:])
                    if saved_username and compare_strings(saved_username, newusername):
                        print("Username already exists. Returning to menu.")
                        time.sleep(2)
                        return False
    except:
        pass

    with open("data.txt", "a") as file:
        file.write("USER:" + newusername + " " + newpassword + "\n")
    set_current_user(newusername)

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
            with open("data.txt", "r") as file:
                while True:
                    line = file.readline()
                    if not line:
                        break
                    if line.startswith("USER:"):
                        saved_username, saved_password = manual_parse_line(line[5:])
                        if saved_username and compare_strings(saved_username, username) and compare_strings(saved_password, password):
                            found = True
                            break
        except:
            print("No registered users found.")
            return False

        if found:
            set_current_user(username)
            print("Login Successful")
            time.sleep(2)
            return True
        else:
            attempts -= 1
            print(f"Invalid credentials. Attempts left: {attempts}")
            time.sleep(2)
    return False

# ------------------- Booking -------------------
def book_table():
    tables = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"]
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
            with open("data.txt", "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.startswith("BOOKING:"):
                        record = line[8:].strip().split(",")
                        if record[2] == date_str and record[3] == time_str and record[5] == chosen_table:
                            print("Table already booked.")
                            return
        except:
            pass

        customers = int(input("Enter number of people (max 6): "))
        if customers <= 0 or customers > 6:
            print("Number of people must be between 1 and 6.")
            return

        with open("data.txt", "a") as f:
            f.write(f"BOOKING:{user},{name},{date_str},{time_str},{customers},{chosen_table}\n")

        print("Booking successful!")

    except ValueError:
        print("Invalid date/time format.")

# ------------------- Ordering -------------------
def load_menu():
    items = []
    try:
        with open("menu.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith("["):
                    i = 0
                    while line[i] != ']':
                        i += 1
                    j = i + 2
                    while line[j] == ' ':
                        j += 1
                    k = j
                    while line[k] != ' ':
                        k += 1
                    item_name = line[j:k]
                    m = k
                    while line[m] == ' ':
                        m += 1
                    price_str = line[m:string_length(line)]
                    price = 0.0
                    dot_seen = False
                    dec_place = 0.1
                    for ch in price_str:
                        if ch == '\n':
                            break
                        if ch == '.':
                            dot_seen = True
                        elif '0' <= ch <= '9':
                            if not dot_seen:
                                price = price * 10 + (ord(ch) - ord('0'))
                            else:
                                price += (ord(ch) - ord('0')) * dec_place
                                dec_place *= 0.1
                    items.append((item_name, price))
    except:
        print("Menu file not found.")
    return items

def place_order():
    print("------ FOOD ORDERING ------")
    menu = load_menu()
    if not menu:
        return

    user = get_current_user()
    booking_info = ""
    try:
        with open("data.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith("BOOKING:") and line[8:].startswith(user + ","):
                    booking_info = line[8:].strip()
    except:
        print("No current booking found. Please book a table first.")
        return

    if booking_info == "":
        print("No valid booking under your account.")
        return

    total = 0
    order_details = []

    i = 0
    while i < string_length(menu):
        print(f"{i + 1}. {menu[i][0]} - RM{menu[i][1]:.2f}")
        i += 1

    while True:
        try:
            choice = int(input("Enter item number to order (0 to finish): "))
            if choice == 0:
                break
            if not (1 <= choice <= string_length(menu)):
                print("Invalid item number.")
                continue

            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be at least 1.")
                continue

            selected_item = menu[choice - 1]
            order_details.append((selected_item[0], selected_item[1], qty))
            total += selected_item[1] * qty

        except:
            print("Invalid input.")

    with open("data.txt", "a") as f:
        for item in order_details:
            f.write(f"ORDER:{booking_info},{item[0]},{item[1]},{item[2]}\n")
        f.write(f"TOTAL:{user},{total:.2f}\n")

    print(f"Order recorded. Total: RM{total:.2f}")

# ------------------- Receipt & History -------------------
def generate_receipt():
    user = get_current_user()
    try:
        with open("data.txt", "r") as f:
            found = False
            print("------ RECEIPT ------")
            total = ""
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith("ORDER:"):
                    parts = line[6:].strip().split(",")
                    if parts[0] != user:
                        continue
                    name, date, time, _, table = parts[1:6]
                    item, price, qty = parts[6], float(parts[7]), int(parts[8])
                    print(f"Customer: {name} | Table: {table} | {item} x{qty} @ RM{price:.2f} = RM{price * qty:.2f}")
                    found = True
                elif line.startswith("TOTAL:"):
                    p = line[6:].strip().split(",")
                    if compare_strings(p[0], user):
                        total = p[1]
            if found:
                print(f"Total: RM{total}")
            else:
                print("No receipt found for this account.")
    except:
        print("No receipt found. Please order first.")

def display_records():
    user = get_current_user()
    try:
        print("------ HISTORICAL BOOKINGS ------")
        with open("data.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith("BOOKING:") and line[8:].startswith(user + ","):
                    print("Booking:", line[8:].strip())
                elif line.startswith("ORDER:"):
                    if line[6:].startswith(user + ","):
                        print("Order:", line[6:].strip())
    except:
        print("No historical records found.")

# ------------------- Menu UI -------------------
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
        except:
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
            set_current_user("")
            time.sleep(1)
            break

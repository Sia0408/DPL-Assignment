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
        with open("session.txt", "r") as f:
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
        with open("session.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if not line.startswith("CURRENT_USER:"):
                    lines.append(line)
    except:
        pass
    with open("session.txt", "w") as f:
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
        with open("users.txt", "r") as file:
            for line in file:
                saved_username, _ = manual_parse_line(line)
                if saved_username and compare_strings(saved_username, newusername):
                    os.system('cls')
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                    time.sleep(2)
                    os.system('cls')
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\tUsername already exists. Back to menu and try register another one.")
                    time.sleep(3)
                    return False
    except FileNotFoundError:
        pass  # File doesn't exist yet, so we can register

    with open("users.txt", "a") as file:
        file.write(newusername + " " + newpassword + "\n")

    os.system('cls')
    print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
    time.sleep(2)
    os.system('cls')
    print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tSuccessfully Registered.")
    time.sleep(2)
    return True

def login():
    attempts = 4
    while attempts > 0:
        os.system('cls')
        username = input("Enter your username : ")
        password = input("Enter your password : ")
        os.system('cls')
        found = False

        try:
            with open("users.txt", "r") as file:
                while True:
                    line = file.readline()
                    if not line:
                        break
                    saved_username, saved_password = manual_parse_line(line)
                    if saved_username and compare_strings(saved_username, username) and compare_strings(saved_password, password):
                        found = True
                        break
        except FileNotFoundError:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\tNo registered users found. Please register first.")
            time.sleep(3)
            return False

        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
        time.sleep(2)

        if found:
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tLogin Successful")
            # Save session
            with open("session.txt", "w") as session_file:
                session_file.write("CURRENT_USER:" + username + "\n")
            time.sleep(2)
            return True
        else:
            attempts -= 1
            os.system('cls')
            if attempts > 0:
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\tInvalid username or password. Attempts left: {attempts}")
                time.sleep(3)
            else:
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\tToo many failed attempts. Returning to menu...")
                time.sleep(3)
                return False

# ------------------- Booking -------------------
def book_table():
    tables = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"]
    print("------ TABLE BOOKING ------")
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
            with open("bookings.txt", "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    record = line.strip().split(",")
                    if record[1] == date_str and record[2] == time_str and record[4] == chosen_table:
                        print("Table already booked.")
                        return
        except:
            pass

        customers = int(input("Enter number of people (max 6): "))
        if customers <= 0 or customers > 6:
            print("Number of people must be between 1 and 6.")
            return

        with open("bookings.txt", "a") as f:
            f.write(f"{user},{date_str},{time_str},{customers},{chosen_table}\n")

        with open("session.txt", "a") as f:
            f.write(f"CURRENT_BOOKING:{user},{date_str},{time_str},{customers},{chosen_table}\n")

        print("Booking successful!")

    except ValueError:
        print("Invalid date/time format.")

# ------------------- Edit Booking -------------------
def edit_table_message():
    user = get_current_user()
    bookings = []

    with open("bookings.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith(user + ","):
                bookings.append(line)

    if string_length(bookings) == 0:
        print("No bookings found.")
        return

    print("Your bookings:")
    for i in range(string_length(bookings)):
        print(f"{i + 1}. {remove_newline(bookings[i])}")

    choice = int(input("Select a booking to edit (1-{}) : ".format(string_length(bookings))))
    if choice < 1 or choice > string_length(bookings):
        print("Invalid selection.")
        return

    selected = bookings[choice - 1]
    parts = selected.strip().split(",")
    date_str = input("Enter new booking date (YYYY-MM-DD): ")
    time_str = input("Enter new booking time (e.g., 7PM): ")
    customers = input("Enter new number of customers: ")
    chosen_table = input("Enter new table number (1-10): ")

    # Rewrite bookings.txt
    with open("bookings.txt", "r") as f:
        all_lines = []
        while True:
            line = f.readline()
            if not line:
                break
            if compare_strings(remove_newline(line), remove_newline(selected)):
                new_line = f"{user},{date_str},{time_str},{customers},{chosen_table}\n"
                all_lines.append(new_line)
            else:
                all_lines.append(line)

    with open("bookings.txt", "w") as f:
        for line in all_lines:
            f.write(line)

    print("Booking updated.")

# ------------------- Menu & Orders -------------------
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

    with open("orders.txt", "a") as f:
        for item in order_details:
            f.write(f"{user},{item[0]},{item[1]},{item[2]}\n")
        f.write(f"TOTAL:{user},{total:.2f}\nPAID:{user}\n")

    print(f"Order recorded. Total: RM{total:.2f}")

# ------------------- Receipt & Records -------------------
def generate_receipt():
    user = get_current_user()
    order_lines = []
    total = ""
    paid = False

    with open("orders.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith(user + ","):
                order_lines.append(line)
            elif line.startswith("TOTAL:" + user):
                total = remove_newline(line.split(",")[1])
            elif line.startswith("PAID:" + user):
                paid = True
                break  # stop after paid confirmation

    if paid and string_length(order_lines) > 0:
        print("Receipt for", user)
        for line in order_lines:
            parts = line.strip().split(",")
            name = parts[1]
            price = float(parts[2])
            qty = int(parts[3])
            print(f"{name} x{qty} @ RM{price:.2f} = RM{price * qty:.2f}")
        print("Total: RM" + total)
    else:
        print("No paid order found for receipt.")

def display_records():
    user = get_current_user()
    print("\nBooking Records:")
    with open("bookings.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith(user + ","):
                parts = line.strip().split(",")
                print("Date:", parts[1], "Time:", parts[2], "Customers:", parts[3], "Table:", parts[4])

    print("\nOrder History:")
    with open("orders.txt", "r") as f:
        order_lines = []
        paid = False
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith("PAID:" + user):
                paid = True
            elif paid and line.startswith(user + ","):
                print("Order:", remove_newline(line))
            elif line.startswith("TOTAL:") and not line.startswith("TOTAL:" + user):
                paid = False

#--------------------Payment-----------------
receipt = 275.50
correct_mastercard_number = "4261829190642876"
correct_visacard_number = "6176344260817654"

def read_balance(file_name):
    try:
        with open(file_name, "r") as file:
            balance = float(file.readline().strip())
        return balance
    except (FileNotFoundError, ValueError):
        print("Error reading balance from", file_name)
        return None

def write_balance(file_name, new_balance):
    with open(file_name, "w") as file:
        file.write("{:.2f}".format(new_balance))

def card_payment(card_type):
    if card_type == "master":
        correct_number = correct_mastercard_number
        file_name = "Mastercard.txt"
        label = "MasterCard"
    elif card_type == "visa":
        correct_number = correct_visacard_number
        file_name = "Visacard.txt"
        label = "Visacard"
    else:
        return False

    attempts = 4
    while attempts > 0:
        os.system('cls')
        print("----------------------------------------------------------")
        card_number = input(f"Please enter your 16-digit {label} number: ")
        if card_number == correct_number:
            balance = read_balance(file_name)
            if balance is None:
                return False  # fail and go back

            os.system('cls')
            print("----------------------------------------------------------")
            print(f"{label} Balance: RM {balance:.2f}")
            print("Receipt Amount    : RM {:.2f}".format(receipt))
            print("----------------------------------------------------------")

            if balance >= receipt:
                new_balance = balance - receipt
                write_balance(file_name, new_balance)
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                time.sleep(2)
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPayment successful!")
                time.sleep(2)
                os.system('cls')
                print("Remaining Balance: RM {:.2f}".format(new_balance))
                return True
            else:
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                time.sleep(2)
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tInsufficient balance! Payment failed.")
                return False
        else:
            attempts -= 1
            if attempts > 0:
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                time.sleep(2)
                os.system('cls')
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\tIncorrect card number. Attempts left: {attempts}")
                time.sleep(1)
            else:
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\tToo many incorrect attempts. Returning to Payment Method...")
                time.sleep(2)
                return False

def manual_length(s):
    count = 0
    try:
        while True:
            _ = s[count]
            count += 1
    except IndexError:
        return count

def ambank_payment():
    attempts = 4
    while attempts > 0:
        os.system('cls')
        acc_number = input("Enter your Ambank 10-digit account number: ").strip()
        pin = input("Enter your 6-digit PIN: ").strip()

        try:
            with open("Ambank.txt", "r") as file:
                lines = file.readlines()

            found = False
            for i in range(manual_length(lines)):
                line = lines[i].strip()
                parts = line.split()
                if manual_length(parts) != 3:
                    continue  # Skip invalid lines
                saved_acc, saved_pin, balance_str = parts
                if acc_number == saved_acc and pin == saved_pin:
                    balance = float(balance_str)
                    if balance >= receipt:
                        new_balance = balance - receipt
                        lines[i] = f"{saved_acc} {saved_pin} {new_balance:.2f}\n"
                        with open("Ambank.txt", "w") as file:
                            file.writelines(lines)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPayment successful!")
                        time.sleep(2)
                        os.system('cls')
                        print("Remaining Balance: RM {:.2f}".format(new_balance))
                        return True
                    else:
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tInsufficient balance.")
                        time.sleep(2)
                        return False
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
            time.sleep(2)
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tInvalid account number or PIN.")
            time.sleep(2)
            attempts -= 1
            if attempts == 0:
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\tToo many failed attempts. Returning to Payment Method.")
                time.sleep(2)
                return False
            else:
                os.system('cls')
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tAttempts remaining: {attempts}")
                time.sleep(2)
        except FileNotFoundError:
            print("Ambank data file not found.")
            return False

def public_bank_payment():
    attempts = 4
    while attempts > 0:
        os.system('cls')
        acc_number = input("Enter your Public Bank 10-digit account number: ").strip()
        pin = input("Enter your 6-digit PIN: ").strip()

        try:
            with open("Publicbank.txt", "r") as file:
                lines = file.readlines()

            found = False
            for i in range(manual_length(lines)):
                line = lines[i].strip()
                parts = line.split()
                if manual_length(parts) != 3:
                    continue  # 跳过格式不对的行
                saved_acc, saved_pin, balance_str = parts
                if acc_number == saved_acc and pin == saved_pin:
                    balance = float(balance_str)
                    if balance >= receipt:
                        new_balance = balance - receipt
                        lines[i] = f"{saved_acc} {saved_pin} {new_balance:.2f}\n"
                        with open("Publicbank.txt", "w") as file:
                            file.writelines(lines)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPayment successful!")
                        time.sleep(2)
                        os.system('cls')
                        print("Remaining Balance: RM {:.2f}".format(new_balance))
                        return True
                    else:
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tInsufficient balance.")
                        time.sleep(2)
                        return False
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
            time.sleep(2)
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tInvalid account number or PIN.")
            time.sleep(2)
            attempts -= 1
            if attempts == 0:
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\tToo many failed attempts. Returning to Payment Method.")
                time.sleep(2)
                return False
            else:
                os.system('cls')
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tAttempts remaining: {attempts}")
                time.sleep(2)
        except FileNotFoundError:
            print("Public Bank data file not found.")
            return False

def tng_payment():
    attempts = 4
    while attempts > 0:
        os.system('cls')
        tng_id = input("Enter your Touch 'n Go account number (e.g., phone number): ").strip()
        pin = input("Enter your 6-digit TNG PIN: ").strip()

        try:
            with open("TNG.txt", "r") as file:
                lines = file.readlines()

            for i in range(manual_length(lines)):
                line = lines[i].strip()
                parts = line.split()
                if manual_length(parts) != 3:
                    continue  # 跳过无效行
                saved_id, saved_pin, balance_str = parts
                if tng_id == saved_id and pin == saved_pin:
                    balance = float(balance_str)
                    if balance >= receipt:
                        new_balance = balance - receipt
                        lines[i] = f"{saved_id} {saved_pin} {new_balance:.2f}\n"
                        with open("TNG.txt", "w") as file:
                            file.writelines(lines)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPayment successful!")
                        time.sleep(2)
                        os.system('cls')
                        print("Remaining Balance: RM {:.2f}".format(new_balance))
                        return True
                    else:
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tInsufficient TNG balance.")
                        time.sleep(2)
                        return False
            # 如果未找到匹配
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
            time.sleep(2)
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tInvalid TNG account or PIN.")
            time.sleep(2)
            attempts -= 1
            if attempts == 0:
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\tToo many failed attempts. Returning to Payment Method.")
                time.sleep(2)
                return False
            else:
                os.system('cls')
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tAttempts remaining: {attempts}")
                time.sleep(2)
        except FileNotFoundError:
            print("TNG data file not found.")
            return False
        
def start_payment():
    while True:
        os.system('cls')
        print("----------------------------------------------------------")
        print("                                        - left RM {:.2f} -".format(receipt))
        print("----------------------------------------------------------")
        print("                        Payment Method                    ")
        print("                         1. Card                          ")
        print("                         2. Bank                          ")
        print("                         3. Others                        ")
        print("                         4. Back                          ")
        print("----------------------------------------------------------")
        try:
            choice2 = int(input("Please enter your payment method (1-4): "))
            if choice2 not in [1, 2, 3, 4]:
                print("Invalid choice. Please enter a number from 1 to 4.")
                time.sleep(1)
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            time.sleep(1)
            continue

        # --- Exit ---
        if choice2 == 4:
            break

        if choice2 == 1:
            while True:
                os.system('cls')
                print("----------------------------------------------------------")
                print("                                        - left RM {:.2f} -".format(receipt))
                print("----------------------------------------------------------")
                print("                              Card                        ")
                print("                         1. Mastercard                    ")
                print("                         2. Visacard                      ")
                print("                         3. Back                          ")
                print("----------------------------------------------------------")
                try:
                    card_choice = int(input("Please select your card type (1-3): "))
                    if card_choice == 1:
                        success = card_payment("master")
                        if success:
                            exit()
                        else:
                            break
                    elif card_choice == 2:
                        success = card_payment("visa")
                        if success:
                            exit()
                        else:
                            break
                    elif card_choice == 3:
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                        time.sleep(1)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    time.sleep(1)


        elif choice2 == 2:
            while True:
                os.system('cls')
                print("----------------------------------------------------------")
                print("                                        - left RM {:.2f} -".format(receipt))
                print("----------------------------------------------------------")
                print("                              Bank                        ")
                print("                         1. Ambank Bhd                    ")
                print("                         2. Public Bank Bhd               ")
                print("                         3. Back                          ")
                print("----------------------------------------------------------")
                try:
                    bank_choice = int(input("Please select your bank (1-3): "))
                    if bank_choice == 1:
                        success = ambank_payment()
                        if success:
                            exit()
                        else:
                            break  # return to payment method
                    elif bank_choice == 2:
                        success = public_bank_payment()
                        if success:
                            exit()
                        else:
                            break
                    elif bank_choice == 3:
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                        time.sleep(1)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    time.sleep(1)
                    
        elif choice2 == 3:
            while True:
                os.system('cls')
                print("----------------------------------------------------------")
                print("                                        - left RM {:.2f} -".format(receipt))
                print("----------------------------------------------------------")
                print("                              Others                      ")
                print("                         1. Touch And Go (TNG)            ")
                print("                         2. Back                          ")
                print("----------------------------------------------------------")
                try:
                    other_choice = int(input("Please select a method (1-2): "))
                    if other_choice == 1:
                        success = tng_payment()
                        if success:
                            exit()
                        else:
                            break
                    elif other_choice == 2:
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                        time.sleep(2)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    time.sleep(2)

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
            print("Invalid choice. Please enter a number between 1 and 6.")
        except:
            print("Invalid input. Please enter a valid number.")

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
        print("Invalid choice. Please enter A or B.")
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
            os.system('cls')
            edit_table_message()
            input("Press Enter to continue...")
        elif choice1 == 5:
            os.system('cls')
            start_payment()
            input("Press Enter to continue...")
        elif choice1 == 6:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tLogging out...")
            set_current_user("")
            time.sleep(2)
            break

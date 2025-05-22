import os
import time
import datetime

def custom_strip(s):
    
    if s == "":
        return ""
    while s.startswith(" ") or s.startswith("\n"):
        s = s[1:]
    while s.endswith(" ") or s.endswith("\n"):
        s = s[:-1]
    return s

def custom_split(s, delimiter):
    
    result = []
    temp = ""
    for i in range(len(s)):
        if s[i] == delimiter:
            result.append(temp)
            temp = ""
        else:
            temp += s[i]
    result.append(temp)
    return result


def register_admin():
    print("========== Admin Registration ==========")
    name = input("> Enter new admin name >  ")
    name = custom_strip(name)
    password = input("> Enter new admin password >  ")
    password = custom_strip(password)

    try:
        with open("admin.txt", "r") as file:
            content = file.read()
            lines = []
            line = ""
            for c in content:
                if c == "\n":
                    lines.append(custom_strip(line))
                    line = ""
                else:
                    line += c
            if line != "":
                lines.append(custom_strip(line))
    except FileNotFoundError:
        lines = ["Name           Password"]

    def is_admin_exists(line):
        parts = []
        for p in custom_split(line, ' '):
            if p != "":
                parts.append(p)
        return len(parts) >= 2 and parts[0] == name

    exists = False
    for l in lines[1:]:
        if is_admin_exists(l):
            exists = True
            break

    if exists:
        print("Admin already exists.")
        time.sleep(2)
        return

    space_num = 15 - len(name)
    if space_num < 1:
        space_num = 1
    spaces = " " * space_num
    new_line = name + spaces + password
    lines.append(new_line)

    with open("admin.txt", "w") as file:
        for l in lines:
            file.write(l + "\n")

    print("\n" * 12 + "\t\t\t\t\t\t\tAdmin " + name + " registered successfully !")
    time.sleep(2)

def admin_login():
    print("\n========== Admin Login ==========")
    name = input("> Enter admin name > ")
    name = custom_strip(name)
    password = input("> Enter password > ")
    password = custom_strip(password)

    attempts = 0
    while attempts < 3:
        try:
            with open("admin.txt", "r") as file:
                skip = True
                line = ""
                logged_in = False
                content = file.read()
                for ch in content:
                    if ch == "\n":
                        line = custom_strip(line)
                        if skip:
                            skip = False
                        elif line != "":
                            parts = line.split()
                            if len(parts) >= 2:
                                stored_name = parts[0]
                                stored_pass = parts[1]
                                if stored_name == name and stored_pass == password:
                                    print(f"Welcome, {name}!")
                                    time.sleep(2)
                                    admin_menu()
                                    return
                        line = ""
                    else:
                        line += ch
                if line != "" and not skip:
                    parts = line.split()
                    if len(parts) >= 2:
                        stored_name = parts[0]
                        stored_pass = parts[1]
                        if stored_name == name and stored_pass == password:
                            print(f"\n" * 12 + "\t\t\t\t\t\t\tWelcome, {name}!")
                            time.sleep(2)
                            admin_menu()
                            return

            print("\n" * 12 + "\t\t\t\t\t\t\tInvalid admin credentials.")
            time.sleep(2)
            attempts += 1
            if attempts == 3:
                print("\n" * 12 + "\t\t\t\t\t\t\tToo many failed attempts. Terminating...")
                time.sleep(2)
                return
        except FileNotFoundError:
            print("\n" * 12 + "\t\t\t\t\t\t\tNo admin data found. Please register an admin first.")
            time.sleep(2)
            return

def admin_menu():
    while True:
        print("--------------------------------------------------")
        print("|                  Admin Menu                    |")
        print("--------------------------------------------------")
        print("|                 1. Display Menu                |")
        print("|                 2. Edit Product                |")
        print("|                 3. Edit Record                 |")
        print("|                 4. Display Record              |")
        print("|                 5. Exit                        |")
        print("--------------------------------------------------")
        choice = input("> Choose an option > ")

        if choice == "1":
            display_menus()
        elif choice == "2":
            edit_product()
        elif choice == "3":
            edit_record()
        elif choice == "4":
            display_record()
        elif choice == "5":
            print("\n" * 12 + "\t\t\t\t\t\t\tReturning to main menu...")
            time.sleep(2)
            break
        else:
            print("\n" * 12 + "\t\t\t\t\t\t\tInvalid choice.")


def display_menus():
    print("\n----------- Restaurant Menu ----------")
    try:
        with open("menu.txt", "r") as file:
            content = file.read()
            if content == "":
                print("\n" * 12 + "\t\t\t\t\t\t\tMenu is empty.")
                time.sleep(2)
                return
            line = ""
            for c in content:
                if c == "\n":
                    line = custom_strip(line)
                    if line != "":
                        print(line)
                    line = ""
                else:
                    line += c
    except FileNotFoundError:
        print("\n" * 12 + "\t\t\t\t\t\t\tMenu not found.")
        time.sleep(2)


def edit_product():
    while True:
        print("--------------------------------------------------")
        print("|                Edit Product Menu               |")
        print("--------------------------------------------------")
        print("|                 1. Add Product                 |")
        print("|                 2. Update Product              |")
        print("|                 3. Delete Product              |")
        print("|                 4. Exit                        |")
        print("--------------------------------------------------")
        choice = custom_strip(input("> Choose an option > "))

        try:
            with open("menu.txt", "r") as file:
                lines = []
                current_line = ""
                content = file.read()
                for c in content:
                    if c == "\n":
                        lines.append(current_line)
                        current_line = ""
                    else:
                        current_line += c
                if current_line != "":
                    lines.append(current_line)
        except FileNotFoundError:
            lines = []

        if len(lines) == 0:
            lines.append("No  Product        Price (RM)")

        if choice == "1":
            while True:
                prod_num = custom_strip(input("Enter product number > "))
                valid_num = True
                for ch in prod_num:
                    if ch < '0' or ch > '9':
                        valid_num = False
                        break
                if not valid_num or prod_num == "":
                    print("\n" * 12 + "\t\t\t\t\t\t\tInvalid input. Please enter digits only.")
                    time.sleep(2)
                else:
                    break

            while True:
                prod_name = custom_strip(input("Enter product name > "))
                valid_name = True
                for ch in prod_name:
                    if ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ":
                        valid_name = False
                        break
                if not valid_name or prod_name == "":
                    print("\n" * 12 + "\t\t\t\t\t\t\tInvalid input. Please enter letters only.")
                    time.sleep(2)
                else:
                    break

            while True:
                prod_price = custom_strip(input("Enter price(RM) (e.g., 12.50) > "))
                dot_count = 0
                valid_price = True
                if prod_price == "":
                    valid_price = False
                else:
                    for i in range(len(prod_price)):
                        ch = prod_price[i]
                        if ch == ".":
                            dot_count += 1
                            if dot_count > 1:
                                valid_price = False
                                break
                        elif ch < "0" or ch > "9":
                            valid_price = False
                            break
                if not valid_price:
                    print("\n" * 12 + "\t\t\t\t\t\t\tInvalid price format.")
                    time.sleep(2)
                else:
                    break

            exist_flag = False
            for l in lines[1:]:
                if l.startswith("[" + prod_num + "]"):
                    exist_flag = True
                    break
            if exist_flag:
                print("\n" * 12 + "\t\t\t\t\t\t\tProduct number already exists.")
                time.sleep(2)
                continue

            space_num = 15 - len(prod_name)
            if space_num < 1:
                space_num = 1
            spaces = " " * space_num
            new_line = "[" + prod_num + "] " + prod_name + spaces + prod_price
            lines.append(new_line)
            print("\n" * 12 + "\t\t\t\t\t\t\tProduct added successfully.")
            time.sleep(2)

        elif choice == "2":
            prod_num = custom_strip(input("Enter product number to update > "))
            found = False
            for i in range(1, len(lines)):
                if lines[i].startswith("[" + prod_num + "]"):
                    found = True
                    print("Current: " + lines[i])
                    new_name = custom_strip(input("Enter new name (leave blank to keep current) > "))
                    new_price = custom_strip(input("Enter new price (leave blank to keep current) > "))

                    line = lines[i]
                    idx = line.find("]") + 1
                    rest = custom_strip(line[idx:])
                    parts = rest.split()
                    current_name = parts[0]
                    current_price = parts[-1]

                    if new_name == "":
                        new_name = current_name
                    if new_price == "":
                        new_price = current_price

                    space_num = 15 - len(new_name)
                    if space_num < 1:
                        space_num = 1
                    spaces = " " * space_num
                    lines[i] = "[" + prod_num + "] " + new_name + spaces + new_price
                    print("\n" * 12 + "\t\t\t\t\t\t\tProduct updated.")
                    time.sleep(2)
                    break
            if not found:
                print("\n" * 12 + "\t\t\t\t\t\t\tProduct number not found.")
                time.sleep(2)

        elif choice == "3":
            prod_num = custom_strip(input("Enter product number to delete > "))
            found = False
            new_lines = [lines[0]]
            for i in range(1, len(lines)):
                if lines[i].startswith("[" + prod_num + "]"):
                    found = True
                    print("Deleted: " + lines[i])
                    continue
                new_lines.append(lines[i])
            if not found:
                print("\n" * 12 + "\t\t\t\t\t\t\tProduct number not found.")
                time.sleep(2)
            else:
                lines = new_lines

        elif choice == "4":
            break

        else:
            print("\n" * 12 + "\t\t\t\t\t\t\tInvalid option.")
            time.sleep(2)
            continue

        with open("menu.txt", "w") as file:
            for l in lines:
                file.write(l + "\n")


def display_record():
    print("\n-------------------| Booking Records |-------------------")
    try:
        with open("bookings.txt", "r") as file:
            content = file.read()

        if content.strip() == "":
            print("No booking records found.")
            return

        print("{:<15}{:<15}{:<10}{:<10}{}".format("Name", "Date", "Time", "People", "Table"))
        print("-" * 65)

        lines = content.strip().split("\n")
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 5:
                print("{:<15}{:<15}{:<10}{:<10}{}".format(parts[0], parts[1], parts[2], parts[3], parts[4]))
            else:
                print("\n" * 12 + "\t\t\t\t\t\t\tInvalid line format:", line)
                time.sleep(2)
    except:
        print("\n" * 12 + "\t\t\t\t\t\t\tNo booking records found.")
        time.sleep(2)


def edit_record():
    print("\n----------- Edit Booking Record ----------")
    name_to_edit = input("> Enter the name to edit > ").strip()
    updated_lines = []
    found = False

    try:
        with open("bookings.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 5 and parts[0].strip() == name_to_edit:
                found = True
                print("Current record:")
                print("Name:", parts[0])
                print("Date:", parts[1])
                print("Time:", parts[2])
                print("People:", parts[3])
                print("Table:", parts[4])

                new_name = input("Enter new name (leave blank to keep current) > ").strip()
                new_date = input("Enter new date (leave blank to keep current) > ").strip()
                new_time = input("Enter new time (leave blank to keep current) > ").strip()
                new_people = input("Enter new number of people (leave blank to keep current) > ").strip()
                new_table = input("Enter new table (leave blank to keep current) > ").strip()

                if new_name == "":
                    new_name = parts[0]
                if new_date == "":
                    new_date = parts[1]
                if new_time == "":
                    new_time = parts[2]
                if new_people == "":
                    new_people = parts[3]
                if new_table == "":
                    new_table = parts[4]

                updated_line = new_name + "," + new_date + "," + new_time + "," + new_people + "," + new_table
                updated_lines.append(updated_line)
                print("\n" * 12 + "\t\t\t\t\t\t\tRecord updated.")
                time.sleep(2)
            else:
                updated_lines.append(line.strip())

        if not found:
            print("\n" * 12 + "\t\t\t\t\t\t\tRecord not found.")
            time.sleep(2)

        with open("bookings.txt", "w") as file:
            for line in updated_lines:
                file.write(line + "\n")

    except FileNotFoundError:
        print("\n" * 12 + "\t\t\t\t\t\t\tNo booking records found.")
        time.sleep(2)



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
    result = ""
    i = 0
    while True:
        try:
            if s[i] == "\n":
                break
            result += s[i]
            i += 1
        except IndexError:
            break
    return result


def manual_parse_line(line):
    line = remove_newline(line)
    i = 0
    while i < string_length(line) and line[i] != " ":
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
            for line in f:
                if not line.startswith("CURRENT_USER:"):
                    lines.append(line)
    except:
        pass
    with open("session.txt", "w") as f:
        for l in lines:
            f.write(l)
        f.write("CURRENT_USER:" + username + "\n")

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
                if saved_username == newusername:
                    os.system('cls')
                    print("\n" * 12 + "\t\t\t\t\t\t\tProcessing")
                    time.sleep(2)
                    os.system('cls')
                    print("\n" * 12 + "\t\t\tUsername already exists. Back to menu and try register another one.")
                    time.sleep(3)
                    return False
    except FileNotFoundError:
        pass 

    with open("users.txt", "a") as file:
        file.write(newusername + " " + newpassword + "\n")

    os.system('cls')
    print("\n" * 12 + "\t\t\t\t\t\t\tProcessing")
    time.sleep(2)
    os.system('cls')
    print("\n" * 12 + "\t\t\t\t\t\t\tSuccessfully Registered.")
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
                for line in file:
                    saved_username, saved_password = manual_parse_line(line)
                    if saved_username == username and saved_password == password:
                        found = True
                        break
        except FileNotFoundError:
            print("\n" * 12 + "\t\t\t\tNo registered users found. Please register first.")
            time.sleep(3)
            return False

        print("\n" * 12 + "\t\t\t\t\t\t\tProcessing")
        time.sleep(2)

        if found:
            os.system('cls')
            print("\n" * 12 + "\t\t\t\t\t\t\tLogin Successful")
            
            with open("session.txt", "w") as session_file:
                session_file.write("CURRENT_USER:" + username + "\n")
            time.sleep(2)
            return True
        else:
            attempts -= 1
            os.system('cls')
            if attempts > 0:
                print(f"\n" * 12 + f"\t\t\t\tInvalid username or password. Attempts left: {attempts}")
                time.sleep(3)
            else:
                print("\n" * 12 + "\t\t\t\tToo many failed attempts. Returning to menu...")
                time.sleep(3)
                return False

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
                for line in f:
                    record = line.strip().split(",")
                    if len(record) == 5 and record[1] == date_str and record[2] == time_str and record[4] == chosen_table:
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


def edit_table_message():
    current_user = get_current_user()
    user_bookings = []

    with open("bookings.txt", "r") as file:
        line = file.readline()
        while line:
            if line.startswith(current_user + ","):
                user_bookings.append(line)
            line = file.readline()

    if string_length(user_bookings) == 0:
        print("No bookings found.")
        return

    print("Your bookings:")
    index = 0
    while index < string_length(user_bookings):
        print(f"{index + 1}. {remove_newline(user_bookings[index])}")
        index += 1

    try:
        selection = int(input("Select a booking to edit (1-{}): ".format(string_length(user_bookings))))
    except:
        print("Invalid input.")
        return

    if selection < 1 or selection > string_length(user_bookings):
        print("Invalid selection.")
        return

    selected_booking = user_bookings[selection - 1]
    booking_parts = selected_booking.strip().split(",")

    new_date = input("Enter new booking date (YYYY-MM-DD): ")
    new_time = input("Enter new booking time (e.g., 7PM): ")
    new_customers = input("Enter new number of customers: ")
    new_table = input("Enter new table number (1-10): ")

    updated_lines = []

    with open("bookings.txt", "r") as file:
        line = file.readline()
        while line:
            if compare_strings(remove_newline(line), remove_newline(selected_booking)):
                new_line = f"{current_user},{new_date},{new_time},{new_customers},{new_table}\n"
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)
            line = file.readline()

    with open("bookings.txt", "w") as file:
        for l in updated_lines:
            file.write(l)

    print("Booking updated.")


def load_menu():
    menu_items = []
    try:
        with open("menu.txt", "r") as file:
            line = file.readline()
            while line:
                if line.startswith("["):
                    name_start = line.find("]") + 2
                    while line[name_start] == ' ':
                        name_start += 1
                    name_end = name_start
                    while line[name_end] != ' ' and name_end < string_length(line):
                        name_end += 1
                    item_name = line[name_start:name_end]

                    price_start = name_end
                    while price_start < string_length(line) and line[price_start] == ' ':
                        price_start += 1
                    price_text = line[price_start:].strip()

                    try:
                        item_price = float(price_text)
                        menu_items.append((item_name, item_price))
                    except:
                        pass
                line = file.readline()
    except:
        print("Menu file not found.")
    return menu_items


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
        print(str(i + 1) + ". " + menu[i][0] + " - RM" + format(menu[i][1], ".2f"))
        i += 1

    while True:
        try:
            choice = int(input("Enter item number to order (0 to finish): "))
            if choice == 0:
                break
            if choice < 1 or choice > string_length(menu):
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
            f.write(user + "," + item[0] + "," + str(item[1]) + "," + str(item[2]) + "\n")
        f.write("TOTAL:" + user + "," + format(total, ".2f") + "\nPAID:" + user + "\n")

    print("Order recorded. Total: RM" + format(total, ".2f"))


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
                break

    if paid and string_length(order_lines) > 0:
        print("Receipt for " + user)
        for line in order_lines:
            parts = line.strip().split(",")
            name = parts[1]
            price = float(parts[2])
            qty = int(parts[3])
            print(name + " x" + str(qty) + " @ RM" + format(price, ".2f") + " = RM" + format(price * qty, ".2f"))
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


correct_mastercard_number = "4261829190642876"
correct_visacard_number = "6176344260817654"
receipt = 0.0
target_username = get_current_user()

prefix = "TOTAL:"
i = 0
while True:
    try:
        ch = target_username[i]
        prefix += ch
        i += 1
    except:
        break
prefix += ","

f = open("orders.txt", "r")
line = f.readline()

while line != "":
    match = True
    a = 0

    while True:
        try:
            prefix_ch = prefix[a]
            line_ch = line[a]
        except:
            match = False
            break

        if prefix_ch != line_ch:
            match = False
            break

        a += 1
        try:
            temp = prefix[a]
        except:
            break  

    if match:
        number_str = ""
        has_dot = False
        while True:
            try:
                ch = line[a]
            except:
                break

            if (ch >= '0' and ch <= '9') or ch == '.':
                if ch == '.':
                    has_dot = True
                number_str += ch
                a += 1
            else:
                break

        int_part = 0
        dec_part = 0
        dec_length = 0
        i = 0
        in_decimal = False

        while True:
            try:
                ch = number_str[i]
            except:
                break

            if ch == '.':
                in_decimal = True
            elif ch >= '0' and ch <= '9':
                digit = 0
                d = '0'
                while d != ch:
                    digit += 1
                    d = chr(48 + digit)  

                if not in_decimal:
                    int_part = int_part * 10 + digit
                else:
                    dec_part = dec_part * 10 + digit
                    dec_length += 1
            i += 1

        divisor = 1
        i = 0
        while i < dec_length:
            divisor = divisor * 10
            i += 1

        if divisor != 0:
            receipt = int_part + (dec_part / divisor)
        else:
            receipt = int_part

        break

    line = f.readline()

f.close()

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
                return False

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
                time.sleep(2)
                generate_receipt()
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
            os.system('cls')
            print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
            time.sleep(2)
            os.system('cls')
            if attempts > 0:
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\tIncorrect card number. Attempts left: {attempts}")
            else:
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\tToo many incorrect attempts. Returning to Payment Method...")
            time.sleep(2)

    return False

def manual_length(s):
    index = 0
    try:
        while True:
            _ = s[index]
            index += 1
    except IndexError:
        return index

def ambank_payment():
    retries = 4
    while retries > 0:
        os.system('cls')
        input_acc = input("Enter your Ambank 10-digit account number: ").strip()
        input_pin = input("Enter your 6-digit PIN: ").strip()

        try:
            with open("Ambank.txt", "r") as f:
                account_data = f.readlines()

            is_verified = False
            for idx in range(manual_length(account_data)):
                line = account_data[idx].strip()
                details = line.split()
                if manual_length(details) != 3:
                    continue  

                stored_acc, stored_pin, raw_balance = details
                if input_acc == stored_acc and input_pin == stored_pin:
                    curr_balance = float(raw_balance)
                    if curr_balance >= receipt:
                        updated_balance = curr_balance - receipt
                        account_data[idx] = f"{stored_acc} {stored_pin} {updated_balance:.2f}\n"
                        with open("Ambank.txt", "w") as f:
                            f.writelines(account_data)

                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPayment successful!")
                        time.sleep(2)
                        os.system('cls')
                        print("Remaining Balance: RM {:.2f}".format(updated_balance))
                        time.sleep(2)
                        generate_receipt()
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
            retries -= 1
            if retries == 0:
                os.system('cls')
                print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\tToo many failed attempts. Returning to Payment Method.")
                time.sleep(2)
                return False
            else:
                os.system('cls')
                print(f"\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tAttempts remaining: {retries}")
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
                    continue  
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
                        time.sleep(2)
                        generate_receipt()
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
                    continue 
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
                        time.sleep(2)
                        generate_receipt()
                        return True
                    else:
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tProcessing")
                        time.sleep(2)
                        os.system('cls')
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tInsufficient TNG balance.")
                        time.sleep(2)
                        return False
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
                            break  
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

def display_menu():
    print("------------------------------------------------------")
    print("                       WELCOME                        ")
    print("------------------------------------------------------")
    print("                   A. Register                        ")
    print("                   B. Log in                          ")
    print("                   C. Exit                          ")
    print("------------------------------------------------------")
    return input("Enter your choice (A/B/C): ")

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

def main():
 while True:  
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==========| Welcome to Restoran Reservation System |==========")
    print("   1. Admin")
    print("   2. User")
    print("   3. Exit")

    choice = input("> Enter your choice > ")

    if choice == '1':
        print("\n1. Register Admin")
        print("2. Login Admin")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_admin()
        elif choice == "2":
            admin_login()
        elif choice == "3":
            print("Exiting system.")
            break
        else:
            print("Invalid selection.")

    elif choice == '2':
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            choice = display_menu()

            if choice.upper() == "A":
                if not register():
                    continue
                if not login():
                    continue
            elif choice.upper() == "B":
                if not login():
                    continue
            elif choice.upper() == "C":
                time.sleep(1)
                break
            else:
                print("Invalid choice. Please enter A ,B, or C.")
                time.sleep(1)
                continue

            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                choice1 = display_main_menu()

                if choice1 == 1:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    book_table()
                    input("Press Enter to continue...")
                elif choice1 == 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    place_order()
                    input("Press Enter to continue...")
                elif choice1 == 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    display_records()
                    input("Press Enter to continue...")
                elif choice1 == 4:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    edit_table_message()
                    input("Press Enter to continue...")
                elif choice1 == 5:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    start_payment()
                    input("Press Enter to continue...")
                elif choice1 == 6:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tLogging out...")
                    set_current_user("")
                    time.sleep(2)
                    break

    elif choice == '3':
        print("Exiting system.")
        break
    else:
        print("Invalid selection.")
        time.sleep(1)
        break


if __name__ == "__main__":
    main()
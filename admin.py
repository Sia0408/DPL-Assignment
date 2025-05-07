def custom_strip(s):
    start = 0
    end = len(s) - 1
    while start <= end and (s[start] == ' ' or s[start] == '\n'):
        start += 1
    while end >= start and (s[end] == ' ' or s[end] == '\n'):
        end -= 1
    result = ''
    for i in range(start, end + 1):
        result += s[i]
    return result

def custom_split(s, delimiter):
    result = []
    current = ''
    for char in s:
        if char == delimiter:
            result.append(current)
            current = ''
        else:
            current += char
    result.append(current)
    return result

def register_admin():
    print("=== Admin Registration ===")
    name = input("Enter new admin name: ")
    name = custom_strip(name)
    password = input("Enter new admin password: ")
    password = custom_strip(password)

    with open("admin.txt", "a") as file:
        file.write(name + "," + password + "\n")
    print("Admin " + name + " registered successfully!")

def admin_login():
    print("\n=== Admin Login ===")
    name = input("Enter admin name: ")
    name = custom_strip(name)
    password = input("Enter password: ")
    password = custom_strip(password)

    try:
        with open("admin.txt", "r") as file:
            content = file.read()
            line = ''
            for char in content:
                if char == '\n':
                    parts = custom_split(custom_strip(line), ',')
                    if len(parts) == 2:
                        stored_name = parts[0]
                        stored_pass = parts[1]
                        if name == stored_name and password == stored_pass:
                            print("Welcome, " + name + "!")
                            admin_menu()
                            return
                    line = ''
                else:
                    line += char
            print("Invalid admin credentials.")
    except FileNotFoundError:
        print("No admin data found. Please register an admin first.")

def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Display Menu")
        print("2. Update Product")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            display_menu()
        elif choice == "2":
            update_product()
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def display_menu():
    print("\n--- Restaurant Menu ---")
    try:
        with open("menu.txt", "r") as file:
            content = file.read()
            if content == "":
                print("Menu is empty.")
                return
            line = ''
            for char in content:
                if char == '\n':
                    parts = custom_split(custom_strip(line), ',')
                    if len(parts) == 2:
                        print(parts[0] + " - RM" + parts[1])
                    line = ''
                else:
                    line += char
    except FileNotFoundError:
        print("Menu not found.")

def update_product():
    print("\n--- Add New Dish ---")
    dish = input("Enter dish name: ")
    dish = custom_strip(dish)
    price = input("Enter price (RM): ")
    price = custom_strip(price)
    with open("menu.txt", "a") as file:
        file.write(dish + "," + price + "\n")
    print("Dish '" + dish + "' added successfully to the menu.")

def main():
    print("=== Welcome to Admin System ===")
    master_password = input("Enter system password to proceed (Hint: 12345): ")
    master_password = custom_strip(master_password)

    if master_password != "12345":
        print("Access denied. Wrong password.")
        return

    while True:
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

if __name__ == "__main__":
    main()

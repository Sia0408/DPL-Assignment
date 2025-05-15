def custom_strip(s):
    return s.strip(' \n')

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

    try:
        with open("admin.txt", "r") as file:
            content = file.read()
            lines = []
            line = ''
            for char in content:
                if char == '\n':
                    lines.append(custom_strip(line))
                    line = ''
                else:
                    line += char
            if line:
                lines.append(custom_strip(line))
    except FileNotFoundError:
        lines = ["Name           Password"]

    def is_admin_exists(line):
        parts = [p for p in custom_split(line, ' ') if p]
        return len(parts) >= 2 and parts[0] == name

    if any(map(is_admin_exists, lines[1:])):
        print("Admin already exists.")
        return

    space_count = 15 - len(name)
    spaces = ' ' * max(space_count, 1)
    new_line = name + spaces + password
    lines.append(new_line)

    with open("admin.txt", "w") as file:
        for line in lines:
            file.write(line + "\n")

    print("Admin " + name + " registered successfully!")


def admin_login():
    print("\n=== Admin Login ===")
    name = input("Enter admin name: ")
    name = custom_strip(name)
    password = input("Enter password: ")
    password = custom_strip(password)

    failed_attempts = 0
    while failed_attempts < 3:
        try:
            with open("admin.txt", "r") as file:
                line = ''
                skip_header = True
                for char in file.read():
                    if char == '\n':
                        line = custom_strip(line)
                        if skip_header:
                            skip_header = False
                        elif line.strip():
                            stored_name, *rest = line.split()
                            if rest and (stored_name, rest[0]) == (name, password):
                                print(f"Welcome, {name}!")
                            admin_menu()
                            return
                        line = ''
                    else:
                        line += char
            print("Invalid admin credentials.")
            failed_attempts += 1
            if failed_attempts == 3:
                print("Too many failed attempts. Terminating...")
                return
        except FileNotFoundError:
            print("No admin data found. Please register an admin first.")
            return


def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Display Menu")
        print("2. Edit Product")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            display_menu()
        elif choice == "2":
            edit_product()
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
                    line = custom_strip(line)
                    if line != "":
                        print(line)
                    line = ''
                else:
                    line += char
    except FileNotFoundError:
        print("Menu not found.")


def edit_product():
    while True:
        print("\n--- Edit Product Menu ---")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Exit")
        choice = custom_strip(input("Choose an option: "))

        try:
            with open("menu.txt", "r") as file:
                lines = []
                current = ''
                for char in file.read():
                    if char == '\n':
                        lines.append(current)
                        current = ''
                    else:
                        current += char
                if current != '':
                    lines.append(current)
        except FileNotFoundError:
            lines = []

        if len(lines) == 0:
            lines.append("No  Product        Price (RM)")

        if choice == "1":
            while True:
                product_number = custom_strip(input("Enter product number : "))
                is_valid = True
                for char in product_number:
                    if char < '0' or char > '9':
                        is_valid = False
                        break
                if not is_valid or product_number == "":
                    print("Invalid input. Please enter digits only.")
                else:
                    break

            while True:
                product_name = custom_strip(input("Enter product name : "))
                is_valid = True
                for char in product_name:
                    if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ':
                        is_valid = False
                        break
                if not is_valid or product_name == "":
                    print("Invalid input. Please enter letters only.")
                else:
                    break

            while True:
                product_price = custom_strip(input("Enter price(RM) (e.g., 12.50): "))
                dot_count = 0
                is_valid = True
                if product_price == "":
                    is_valid = False
                else:
                    for i, char in enumerate(product_price):
                        if char == '.':
                            dot_count += 1
                            if dot_count > 1:
                                is_valid = False
                                break
                        elif char < '0' or char > '9':
                            is_valid = False
                            break
                if not is_valid:
                    print("Invalid price format.")
                else:
                    break

            exists = False
            for line in lines[1:]:
                if line.startswith("[" + product_number + "]"):
                    exists = True
                    break
            if exists:
                print("Product number already exists.")
                continue

            space_count = 15 - len(product_name)
            spaces = ' ' * max(space_count, 1)
            new_line = "[" + product_number + "] " + product_name + spaces + product_price
            lines.append(new_line)
            print("Product added successfully.")


        elif choice == "2":
            prod_num = custom_strip(input("Enter product number to update: "))
            found = False
            for i in range(1, len(lines)):
                if lines[i].startswith("[" + prod_num + "]"):
                    found = True
                    print("Current: " + lines[i])
                    new_name = custom_strip(input("Enter new name (leave blank to keep current): "))
                    new_price = custom_strip(input("Enter new price (leave blank to keep current): "))

                    line = lines[i]
                    end_num = line.find("]") + 1
                    parts = custom_strip(line[end_num:]).split()
                    current_name = parts[0]
                    current_price = parts[-1]

                    if new_name == "":
                        new_name = current_name
                    if new_price == "":
                        new_price = current_price

                    space_count = 15 - len(new_name)
                    spaces = ' ' * max(space_count, 1)
                    lines[i] = "[" + prod_num + "] " + new_name + spaces + new_price
                    print("Product updated.")
                    break
            if not found:
                print("Product number not found.")

        elif choice == "3":
            prod_num = custom_strip(input("Enter product number to delete: "))
            found = False
            new_lines = [lines[0]] 
            for i in range(1, len(lines)):
                if lines[i].startswith("[" + prod_num + "]"):
                    found = True
                    print("Deleted: " + lines[i])
                    continue
                new_lines.append(lines[i])
            if not found:
                print("Product number not found.")
            else:
                lines = new_lines

        elif choice == "4":
            break

        else:
            print("Invalid option.")
            continue

        with open("menu.txt", "w") as file:
            for line in lines:
                file.write(line + "\n")

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

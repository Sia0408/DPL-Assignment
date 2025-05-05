def register_admin():
    print("=== Admin Registration ===")
    name = input("Enter new admin name: ").strip()
    password = input("Enter new admin password: ").strip()

    with open("admin.txt", "a") as file:
        file.write(f"{name},{password}\n")
    print(f"Admin {name} registered successfully!")


def admin_login():
    print("\n=== Admin Login ===")
    name = input("Enter admin name: ").strip()
    password = input("Enter password: ").strip()

    try:
        with open("admin.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                stored_name, stored_pass = line.strip().split(",")
                if name == stored_name and password == stored_pass:
                    print(f"Welcome, {name}!")
                    admin_menu()
                    return
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
            menu_items = file.readlines()
            if not menu_items:
                print("Menu is empty.")
            else:
                for line in menu_items:
                    name, price = line.strip().split(",")
                    print(f"{name} - RM{price}")
    except FileNotFoundError:
        print("Menu not found.")


def update_product():
    print("\n--- Add New Dish ---")
    dish = input("Enter dish name: ").strip()
    price = input("Enter price (RM): ").strip()
    with open("menu.txt", "a") as file:
        file.write(f"{dish},{price}\n")
    print(f"Dish '{dish}' added successfully to the menu.")


def main():
    print("=== Welcome to Admin System ===")
    master_password = input("Enter system password to proceed (Hint: 12345): ").strip()

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

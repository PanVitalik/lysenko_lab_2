from model import Model
from view import View

class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()

    def display_menu(self):
        menu_options = {
            "1": "View all data from any table",
            "2": "Search data",
            "3": "Delete Data",
            "4": "Add new user",
            "5": "Add new service",
            "6": "Add new room",
            "7": "Add new room type",
            "8": "Add new ordering service",
            "9": "Update user",
            "10": "Update service",
            "11": "Update room",
            "12": "Update room type",
            "13": "Update ordering service",
            "14": "Generate random users",
            "15": "Generate random services",
            "16": "Generate random rooms",
            "17": "Generate random room types",
            "18": "Generate ordering services",
            "19": "Exit"
        }
        print("\n--- Main Menu ---")
        for key, option in menu_options.items():
            print(f"{key}. {option}")

    def run(self):
        while True:
            # Display menu options to the user
            self.display_menu()
            
            choice = self.view.get_input("Select an option: ")
            
            if choice == "1":
                self.view_all_data()
            elif choice == "2":
                self.search_data()
            elif choice == "3":
                self.delete_entry()
            elif choice == "4":
                self.add_user()
            elif choice == "5":
                self.add_service()
            elif choice == "6":
                self.add_room()
            elif choice == "7":
                self.add_room_type()
            elif choice == "8":
                self.add_ordering_service()
            elif choice == "9":
                self.update_user()
            elif choice == "10":
                self.update_service()
            elif choice == "11":
                self.update_room()
            elif choice == "12":
                self.update_room_type()
            elif choice == "13":
                self.update_ordering_service()
            elif choice == "14":
                self.generate_random_users()
            elif choice == "15":
                self.generate_services()
            elif choice == "16":
                self.generate_rooms()
            elif choice == "17":
                self.generate_room_types()
            elif choice == "18":
                self.generate_ordering_services()
            elif choice == "19":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def view_all_data(self):
        try:
            # Prompt user for table name
            table_name = self.view.get_input("Enter table name to view all data: ")
            
            # Fetch all data from the specified table
            data = self.model.get_data(table_name)

            # Display the fetched data
            if data:
                # self.view.show_data(data)
                if table_name == "users":
                    self.view.show_users(data)
                elif table_name == "services":
                    self.view.show_services(data)
                elif table_name == "rooms":
                    self.view.show_rooms(data)
                elif table_name == "room_type":
                    self.view.show_room_types(data)
                elif table_name == "ordering_services":
                    self.view.show_ordering_services(data)
            else:
                print("No data found or invalid table name.")
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")


    def delete_entry(self):
        try:
            table_name = input("Enter table name: ")
            id = input("Enter record ID: ")
            self.model.delete_data(table_name, id)
        except Exception as e:
            print(f"An error occurred while processing your request: {e}")

    def add_ordering_service(self):
        """Обробка введення для додавання нового запису в таблицю ordering_services."""
        try:
            user_id = int(input("Enter user ID: "))
            service_id = int(input("Enter service ID: "))
            date = input("Enter date (YYYY-MM-DD HH:MM:SS): ")

            self.model.add_ordering_service(user_id, service_id, date)
            print(f"Ordering service for user {user_id} and service {service_id} added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def update_ordering_service(self):
        """Обробка введення для оновлення запису в таблиці ordering_services."""
        try:
            user_id = int(input("Enter user ID: "))
            service_id = int(input("Enter service ID: "))
            date = input("Enter date (YYYY-MM-DD HH:MM:SS): ")
            field = input("Enter field to update (user_id, service_id, data): ")
            new_value = input("Enter new value: ")

            self.model.update_ordering_service(user_id, service_id, field, new_value, date)
            print(f"Ordering service updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def generate_ordering_services(self):
        """Обробка введення для генерації випадкових записів в таблицю ordering_services."""
        try:
            num_records = int(input("Enter the number of ordering services to generate: "))
            self.model.generate_ordering_services(num_records)
        except Exception as e:
            print(f"Error: {e}")


    def add_room_type(self):
        """Збір даних для додавання нового запису в таблицю room_type."""
        try:
            room_type_id = int(self.view.get_input("Enter room type ID: "))
            type = self.view.get_input("Enter room type: ")
            price = int(self.view.get_input("Enter price: "))
            
            self.model.add_room_type(room_type_id, type, price)
        except Exception as e:
            self.view.show_message(f"Error adding room type: {e}")

    def update_room_type(self):
        """Збір даних для оновлення запису в таблицю room_type."""
        try:
            room_type_id = int(self.view.get_input("Enter room type ID to update: "))
            field = self.view.get_input("Enter field to update: ")
            new_value = self.view.get_input("Enter new value: ")
            
            self.model.update_room_type(room_type_id, field, new_value)
        except Exception as e:
            self.view.show_message(f"Error updating room type: {e}")

    def generate_room_types(self):
        """Збір кількості записів для генерації в таблиці room_type."""
        try:
            num_room_types = int(self.view.get_input("Enter the number of room types to generate: "))
            self.model.generate_room_types(num_room_types)
        except Exception as e:
            self.view.show_message(f"Error generating room types: {e}")


    def add_room(self):
        """Додавання нового номера до таблиці rooms."""
        print("Adding a new room")

        # Введення даних від користувача
        room_id = input("Enter room ID: ")
        room_number = input("Enter room number: ")
        room_type_id = input("Enter room type ID: ")
        user_id = input("Enter user ID (if applicable, else leave empty): ")
        check_in_date = input("Enter check-in date (YYYY-MM-DD HH:MM:SS): ")
        check_out_date = input("Enter check-out date (YYYY-MM-DD HH:MM:SS): ")

        # Викликаємо функцію додавання номера
        try:
            self.model.add_room(room_id, room_number, room_type_id, user_id, check_in_date, check_out_date)
        except Exception as e:
            print(f"An error occurred while adding the room: {e}")


    def update_room(self):
        """Збір даних для оновлення запису в таблиці rooms."""
        try:
            room_id = int(self.view.get_input("Enter room ID to update: "))
            field = self.view.get_input("Enter field to update: ")
            new_value = self.view.get_input("Enter new value: ")
            
            self.model.update_room(room_id, field, new_value)
        except Exception as e:
            self.view.show_message(f"Error updating room: {e}")

    def update_ordering_service(self):
        """Збір даних для оновлення запису в таблиці ordering_services."""
        try:
            # Отримуємо дані від користувача через view
            user_id = int(self.view.get_input("Enter user ID: "))
            service_id = int(self.view.get_input("Enter service ID: "))
            field = self.view.get_input("Enter field to update: ")
            new_value = self.view.get_input("Enter new value: ")

            # Виклик методу моделі для оновлення
            self.model.update_ordering_service(user_id, service_id, field, new_value)

            # Повідомлення про успішне оновлення
            self.view.show_message("Ordering service updated successfully.")
        except ValueError:
            self.view.show_message("Invalid input. Please enter valid data.")
        except Exception as e:
            self.view.show_message(f"Error updating ordering service: {e}")


    def generate_rooms(self):
        """Збір кількості записів для генерації в таблиці rooms."""
        try:
            num_rooms = int(self.view.get_input("Enter the number of rooms to generate: "))
            self.model.generate_rooms(num_rooms)
        except Exception as e:
            self.view.show_message(f"Error generating rooms: {e}")


    def update_service(self):
        """Оновлення даних сервісу."""
        try:
            service_id = int(input("Enter service ID to update: "))
            print("What would you like to update?")
            print("1. Service name")
            print("2. Service price")
            choice = input("Enter your choice (1 or 2): ")

            if choice == '1':
                new_service_name = input("Enter new service name: ")
                self.model.update_service(service_id, 'sirvice_name', new_service_name)
                print(f"Service with ID {service_id} updated successfully.")
            elif choice == '2':
                new_price = input("Enter new price: ")
                self.model.update_service(service_id, 'price', new_price)
                print(f"Service with ID {service_id} updated successfully.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter numeric values where required.")
        except Exception as e:
            print(f"Error updating service: {e}")  

    def add_service(self):
        """Додавання нового сервісу."""
        try:
            service_id = int(input("Enter service ID: "))
            service_name = input("Enter service name: ")
            price = int(input("Enter service price: "))
            self.model.add_service(service_id, service_name, price)
            print(f"Service '{service_name}' added successfully.")
        except ValueError:
            print("Invalid input. Please enter numeric values for ID and price.")
        except Exception as e:
            print(f"Error adding service: {e}")

    def generate_services(self):
        """Генерація випадкових сервісів."""
        try:
            num_services = int(input("Enter the number of services to generate: "))
            if num_services <= 0:
                raise ValueError("Number of services must be greater than 0.")
            self.model.generate_services(num_services)
            print(f"{num_services} random services generated successfully.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error generating services: {e}")

    # Функції для кожної операції додавання, оновлення, видалення і т.д.
    def add_user(self):
        try:
            user_id = int(self.view.get_input("Enter user ID: "))
            name = self.view.get_input("Enter name: ")
            phone_number = self.view.get_input("Enter phone number: ")
            self.model.add_user(user_id, name, phone_number)
        except Exception as e:
            self.view.show_message("Invalid input. Try again.")

    def generate_users(self):
        try:
            num_users = int(self.view.get_input("Enter number of users to generate: "))
            self.model.generate_users(num_users)
        except Exception as e:
            self.view.show_message(f"An error occurred during generation: {e}")

    def update_user(self):
        try:
            user_id = int(self.view.get_input("Enter user ID to update: "))
            name = self.view.get_input("Enter new name (leave blank to keep current): ")
            phone_number = self.view.get_input("Enter new phone number (leave blank to keep current): ")
            self.model.update_user(user_id, name or None, phone_number or None)
        except Exception as e:
            self.view.show_message("Invalid input. Try again.")

    def generate_random_users(self):
        """Generates a specified number of random users."""
        try:
            num_users = int(self.view.get_input("Enter the number of users to generate: "))
            self.model.generate_users(num_users)
        except Exception as e:
            print(f"Error: {e}")

    def search_data(self):
        search_type = self.view.get_input("Enter search type (1 for range, 2 for LIKE search): ")
        if search_type == "1":
            table_name = self.view.get_input("Enter table name: ")
            id_field = self.view.get_input("Enter field to filter by: ")
            id_start = int(self.view.get_input("Enter start ID: "))
            id_end = int(self.view.get_input("Enter end ID: "))
            order_field = self.view.get_input("Enter order field: ")
            result = self.model.get_data_in_range(table_name, id_field, id_start, id_end, order_field)
        elif search_type == "2":
            table_name = self.view.get_input("Enter table name: ")
            req_field = self.view.get_input("Enter field to search: ")
            search_req = self.view.get_input("Enter search term: ")
            order_field = self.view.get_input("Enter order field: ")
            result = self.model.get_data_by_field_like(table_name, req_field, search_req, order_field)
        else:
            result = []
            self.view.show_message("Invalid search type.")
        # self.view.show_data(result)
        if result:
            # self.view.show_data(data)
            if table_name == "users":
                self.view.show_users(result)
            elif table_name == "services":
                self.view.show_services(result)
            elif table_name == "rooms":
                self.view.show_rooms(result)
            elif table_name == "room_type":
                self.view.show_room_types(result)
            elif table_name == "ordering_services":
                self.view.show_ordering_services(result)

class View:
    def get_input(self, prompt):
        return input(prompt)

    def show_message(self, message):
        print(message)

    def show_data(self, data):
        try:
            if not data:
                print("No data available to display.")
                return
            
            for row in data:
                print(row)
        
        except Exception as e:
            print(f"An error occurred while displaying the data: {e}")

    def show_users(self, data):
        """Форматований вивід для таблиці users."""
        for row in data:
            print(f"User ID: {row.user_id}\nName: {row.name}\nPhone Number: {row.phone_number}\n")

    def show_services(self, data):
        """Форматований вивід для таблиці services."""
        for row in data:
            print(f"Service ID: {row.service_id}\nService Name: {row.sirvice_name}\nPrice: {row.price}\n")

    def show_rooms(self, data):
        """Форматований вивід для таблиці rooms."""
        for row in data:
            print(f"Room ID: {row.room_id}\nRoom Number: {row.room_number}\n"
                f"Room Type ID: {row.room_type_id}\nUser ID: {row.user_id}\n"
                f"Check-in Date: {row.check_in_date}\nCheck-out Date: {row.check_out_date}\n")

    def show_room_types(self, data):
        """Форматований вивід для таблиці room_type."""
        for row in data:
            print(f"Room Type ID: {row.room_type_id}\nType Name: {row.type}\nPrice: {row.price}\n")

    def show_ordering_services(self, data):
        """Форматований вивід для таблиці ordering_services."""
        for row in data:
            print(f"User ID: {row.user_id}\nService ID: {row.service_id}\nDate: {row.data}\n")


# classes
import pandas as pd
import os
import ast


class MenuItem:
    def __init__(self, name, price, item_type, available=True):
        self.name = name
        self.price = price
        self.item_type = item_type
        self.available = available

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "item_type": self.item_type,
            "available": self.available
        }

    @staticmethod
    def from_dict(data):
        return MenuItem(data['name'], data['price'], data['item_type'], data['available'])

    def __str__(self):
        status = "Available" if self.available else "Unavailable"
        return f"{self.name} ({self.item_type}): ${self.price} - {status}"


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]

    def search_item(self, query):
        return [item for item in self.items if query.lower() in item.name.lower()]

    def display_menu(self):
        foods = [item for item in self.items if item.item_type == 'food']
        drinks = [item for item in self.items if item.item_type == 'drink']

        print("Foods:")
        for food in foods:
            print(
                f" - {food.name}: ${food.price} - {'Available' if food.available else 'Unavailable'}")

        print("\nDrinks:")
        for drink in drinks:
            print(
                f" - {drink.name}: ${drink.price} - {'Available' if drink.available else 'Unavailable'}")

    def save_to_excel(self, filename):
        data = [item.to_dict() for item in self.items]
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    def load_from_excel(self, filename):
        df = pd.read_excel(filename)
        self.items = [MenuItem.from_dict(row) for _, row in df.iterrows()]


class Order:
    def __init__(self, customer, is_online=True):
        self.customer = customer
        self.items = []
        self.is_online = is_online
        self.total_price = 0

    def add_item(self, item):
        self.items.append(item)
        self.total_price += item.price

    def to_dict(self):
        return {
            "customer": self.customer.name,
            "items": [item.to_dict() for item in self.items],
            "is_online": self.is_online,
            "total_price": self.total_price
        }

    @staticmethod
    def from_dict(data, customer):
        order = Order(customer, data['is_online'])
        for item_data in data['items']:
            order.add_item(MenuItem.from_dict(item_data))
        return order

    def __str__(self):
        order_type = "Online" if self.is_online else "In-Person"
        return f"Order for {self.customer.name} ({order_type}): ${self.total_price}"


class Customer:
    def __init__(self, name, is_member=False):
        self.name = name
        self.is_member = is_member
        self.previous_orders = []

    def add_order(self, order):
        self.previous_orders.append(order)

    def view_orders(self):
        for order in self.previous_orders:
            print(order)

    def to_dict(self):
        return {
            "name": self.name,
            "is_member": self.is_member,
            "previous_orders": [order.to_dict() for order in self.previous_orders]
        }

    @staticmethod
    def from_dict(data):

        customer = Customer(data['name'], data['is_member'])
        previous_orders = ast.literal_eval(data['previous_orders'])
        customer.previous_orders = [Order.from_dict(
            order_data, customer) for order_data in previous_orders]
        return customer


class Table:
    def __init__(self, table_id, capacity=4):
        self.table_id = table_id
        self.capacity = capacity
        self.is_reserved = False

    def reserve(self):
        self.is_reserved = True

    def release(self):
        self.is_reserved = False

    def to_dict(self):
        return {"table_id": self.table_id, "capacity": self.capacity, "is_reserved": self.is_reserved}

    @staticmethod
    def from_dict(data):
        table = Table(data['table_id'], data['capacity'])
        table.is_reserved = data['is_reserved']
        return table

    def __str__(self):
        return f"Table {self.table_id}: {'Reserved' if self.is_reserved else 'Available'}"


class Courier:
    def __init__(self, courier_id):
        self.courier_id = courier_id

    def to_dict(self):
        return {"courier_id": self.courier_id}

    @staticmethod
    def from_dict(data):
        return Courier(data['courier_id'])

    def __str__(self):
        return f"Courier {self.courier_id}"


class Restaurant:
    def __init__(self, name, table_count, excel_directory="restaurant_data"):
        self.name = name
        self.menu = Menu()
        self.tables = [Table(i+1) for i in range(table_count)]
        self.couriers = []
        self.orders = []
        self.customers = []
        self.excel_directory = excel_directory
        self.initialize_files()

    def initialize_files(self):
        if not os.path.exists(self.excel_directory):
            os.makedirs(self.excel_directory)

        menu_file = os.path.join(self.excel_directory, "menu.xlsx")
        tables_file = os.path.join(self.excel_directory, "tables.xlsx")
        couriers_file = os.path.join(self.excel_directory, "couriers.xlsx")
        orders_file = os.path.join(self.excel_directory, "orders.xlsx")
        customers_file = os.path.join(self.excel_directory, "customers.xlsx")

        if not os.path.exists(menu_file):
            self.menu.save_to_excel(menu_file)
            print("Menu xlsx created")
        else:
            self.menu.load_from_excel(menu_file)
            print("Menu xlsx loaded")

        if not os.path.exists(tables_file):
            self.save_tables_to_excel(tables_file)
            print("Tables xlsx created")
        else:
            self.load_tables_from_excel(tables_file)
            print("Tables xlsx loaded")

        if not os.path.exists(couriers_file):
            self.save_couriers_to_excel(couriers_file)
            print("Couriers xlsx created")
        else:
            self.load_couriers_from_excel(couriers_file)
            print("Couriers xlsx loaded")

        if not os.path.exists(orders_file):
            self.save_orders_to_excel(orders_file)
            print("Orders xlsx created")
        else:
            self.load_orders_from_excel(orders_file)
            print("Orders xlsx loaded")

        if not os.path.exists(customers_file):
            self.save_customers_to_excel(customers_file)
            print("Customers xlsx created")
        else:
            self.load_customers_from_excel(customers_file)
            print("Customers xlsx loaded")

    def save_data_to_excel(self):
        menu_file = os.path.join(self.excel_directory, "menu.xlsx")
        tables_file = os.path.join(self.excel_directory, "tables.xlsx")
        couriers_file = os.path.join(self.excel_directory, "couriers.xlsx")
        orders_file = os.path.join(self.excel_directory, "orders.xlsx")
        customers_file = os.path.join(self.excel_directory, "customers.xlsx")

        self.menu.save_to_excel(menu_file)
        self.save_tables_to_excel(tables_file)
        self.save_couriers_to_excel(couriers_file)
        self.save_orders_to_excel(orders_file)
        self.save_customers_to_excel(customers_file)
        print("All data saved to Excel")

    def load_data_from_excel(self):
        menu_file = os.path.join(self.excel_directory, "menu.xlsx")
        tables_file = os.path.join(self.excel_directory, "tables.xlsx")
        couriers_file = os.path.join(self.excel_directory, "couriers.xlsx")
        orders_file = os.path.join(self.excel_directory, "orders.xlsx")
        customers_file = os.path.join(self.excel_directory, "customers.xlsx")

        self.menu.load_from_excel(menu_file)
        self.load_tables_from_excel(tables_file)
        self.load_couriers_from_excel(couriers_file)
        self.load_orders_from_excel(orders_file)
        self.load_customers_from_excel(customers_file)

    def save_tables_to_excel(self, filename):
        data = [table.to_dict() for table in self.tables]
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    def load_tables_from_excel(self, filename):
        df = pd.read_excel(filename)
        self.tables = [Table.from_dict(row) for _, row in df.iterrows()]

    def save_couriers_to_excel(self, filename):
        data = [courier.to_dict() for courier in self.couriers]
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    def load_couriers_from_excel(self, filename):
        df = pd.read_excel(filename)
        self.couriers = [Courier.from_dict(row) for _, row in df.iterrows()]

    def save_orders_to_excel(self, filename):
        data = [order.to_dict() for order in self.orders]
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    def load_orders_from_excel(self, filename):
        df = pd.read_excel(filename)
        for _, row in df.iterrows():
            customer_name = row['customer']
            customer = next(
                (c for c in self.customers if c.name == customer_name), None)
            if customer:
                order = Order.from_dict(row, customer)
                self.orders.append(order)

    def save_customers_to_excel(self, filename):
        data = [customer.to_dict() for customer in self.customers]
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    def load_customers_from_excel(self, filename):
        df = pd.read_excel(filename)
        self.customers = [Customer.from_dict(row) for _, row in df.iterrows()]

    def add_courier(self, courier):
        self.couriers.append(courier)

    def add_table(self, table):
        self.tables.append(table)

    def add_order(self, order):
        self.orders.append(order)
        order.customer.add_order(order)

    def add_customer(self, customer):
        self.customers.append(customer)

    def display_tables(self):
        for table in self.tables:
            print(table)


"""# UserInterface"""


class UserInterface:
    def __init__(self, restaurant):
        self.restaurant = restaurant

    def main_menu(self):
        print("Welcome to", self.restaurant.name)
        while True:
            print("\n1. Customer Access\n2. Manager Access\n3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.customer_access()
            elif choice == '2':
                self.manager_access()
            elif choice == '3':
                self.restaurant.save_data_to_excel()
                break
            else:
                print("Invalid choice. Please try again.")

    def customer_access(self):
        print("\n--- Customer Access ---")
        while True:
            print("\n1. View Menu\n2. Search Menu\n3. Place Order\n4. Reserve Table\n5. View Previous Orders\n6. Back")
            choice = input("Choose an option: ")
            if choice == '1':
                self.restaurant.menu.display_menu()
            elif choice == '2':
                query = input("Enter search query: ")
                results = self.restaurant.menu.search_item(query)
                for item in results:
                    print(item)
            elif choice == '3':
                self.place_order()
            elif choice == '4':
                self.reserve_table()
            elif choice == '5':
                self.view_previous_orders()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def place_order(self):
        customer_name = input("Enter your name: ")
        customer = next(
            (c for c in self.restaurant.customers if c.name == customer_name), None)
        if not customer:  # if he isnt my restaurant cumtomers ...
            customer = Customer(customer_name)
            self.restaurant.add_customer(customer)

        ordertype = input(
            "Enter your order type (1 for online, 0 for in-person): ") == '1'
        print("ordertype:", ordertype)
        order = Order(customer, ordertype)
        if ordertype:
            # 'order.is_online = 1 --> express'
            dist = int(
                input("Enter your distance to the restaurant in kilometers: "))
            if dist > 5:
                print(
                    "The restaurant sends the order by courier to a maximum radius of five kilometers.")
                return
        # 'else:'
            # 'order.is_online = 0 --> not express'

        while True:
            item_name = input(
                "Enter the name of the item to add (or 'done' to finish): ")
            if item_name == 'done':
                break
            item = next(
                (i for i in self.restaurant.menu.items if i.name == item_name), None)
            if item:
                if item.available:
                    order.add_item(item)
                    print(f"{item.name} added to order.")
                else:
                    print(f"{item.name} is unavailable.")
            else:
                print("Item not found.")

        if order.items:
            self.restaurant.add_order(order)
            print("Order placed successfully.")

            # Display the bill
            print("\n--- Bill ---")
            for item in order.items:
                print(f"{item.name}: ${item.price}")
            print(f"Total: ${order.total_price}")

            # Choose payment method
            while True:
                payment_method = input(
                    "Choose payment method (cash/online): ").lower()
                if payment_method == 'cash':
                    print("Thank you for your order. You can pay with cash.")
                    break
                elif payment_method == 'online':
                    print(
                        "Thank you for your order. Please follow this link to pay online: [Payment Link]")
                    break
                else:
                    print(
                        "Invalid payment method. Please choose either 'cash' or 'online'.")
        else:
            print("No items in the order. Order not placed.")

    def reserve_table(self):
        for table in self.restaurant.tables:
            print(table)
        table_id = int(input("Enter the table ID to reserve: "))
        table = next(
            (t for t in self.restaurant.tables if t.table_id == table_id), None)
        if table and not table.is_reserved:
            table.reserve()
            print("Table reserved successfully.")
        else:
            print("Table not found or already reserved.")

    def view_previous_orders(self):
        customer_name = input("Enter your name: ")
        customer = next(
            (c for c in self.restaurant.customers if c.name == customer_name), None)
        if customer:
            customer.view_orders()
        else:
            print("Customer not found.")

    def manager_access(self):
        print("\n--- Manager Access ---")
        while True:
            print(
                "\n1. Add Menu Item\n2. Remove Menu Item\n3. View Orders\n4. Add Courier\n5. Add Table\n6. Back")
            choice = input("Choose an option: ")
            if choice == '1':
                self.add_menu_item()
            elif choice == '2':
                self.remove_menu_item()
            elif choice == '3':
                self.view_orders()
            elif choice == '4':
                self.add_courier()
            elif choice == '5':
                self.add_table()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_menu_item(self):
        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        item_type = input("Enter item type (food/drink): ")
        available = input("Is the item available? (yes/no): ").lower() == 'yes'
        item = MenuItem(name, price, item_type, available)
        self.restaurant.menu.add_item(item)
        print("Item added successfully.")

    def remove_menu_item(self):
        name = input("Enter item name to remove: ")
        self.restaurant.menu.remove_item(name)
        print("Item removed successfully.")

    def view_orders(self):
        for order in self.restaurant.orders:
            print(order)

    def add_courier(self):
        courier_id = input("Enter courier ID: ")
        courier = Courier(courier_id)
        self.restaurant.add_courier(courier)
        print("Courier added successfully.")

    def add_table(self):
        table_id = input("Enter table ID: ")
        table = Table(table_id)
        self.restaurant.add_table(table)
        print("Table added successfully.")


"""# Run"""

# Putting It All Together
if __name__ == "__main__":

    k = 10  # table_count
    excel_directory = r"!!!file-address!!!"  # Enter the full path to your file !!!
    restaurant = Restaurant("your Restaurant name ", k, excel_directory)

    ui = UserInterface(restaurant)
    ui.main_menu()

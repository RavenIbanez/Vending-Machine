import turtle # import turtle so we can visualize the vending machine itself

class Item:
    def __init__(self, name, category, price, stock): # lets define our items
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

class VendingMachine: # main class that would define the vending machines operations
    def __init__(self):
        self.items = { # dictionary to store items
            "A1": Item("Coffee", "Hot Drinks", 2.0, 10),
            "A2": Item("Tea", "Hot Drinks", 1.5, 10),
            "B1": Item("Soda", "Cold Drinks", 1.8, 10),
            "B2": Item("Water", "Cold Drinks", 1.0, 10),
            "C1": Item("Chocolate", "Snacks", 1.2, 10),
            "C2": Item("Chips", "Snacks", 1.5, 10),
        }
        self.slot_positions = { # dictionary in mapping the item codes for the turtle graphics
            "A1": (-120, 150), "A2": (0, 150),
            "B1": (-120, 30), "B2": (0, 30),
            "C1": (-120, -90), "C2": (0, -90)
        }

    def display_menu(self): # categorize the items when displayed
        print("Welcome to the Vending Machine!\n") 
        categories = {}
        for code, item in self.items.items():
            categories.setdefault(item.category, []).append((code, item))

        for category, items in categories.items():
            print(f"-- {category} --")
            for code, item in items:
                print(f"{code}: {item.name} (${item.price}) [{item.stock} in stock]")
            print()

    def select_item(self):
        while True:
            code = input("Enter the code of the item you want to buy: ").upper() # let the user choose an item, also would check if an item is in stock
            if code in self.items:
                item = self.items[code]
                if item.stock > 0:
                    return code
                else:
                    print("Sorry, this item is out of stock.")
            else:
                print("Invalid code. Please try again.")

    def process_payment(self, item): # handles the payment; checks how much money is put in, and it also calculates the money. 
        while True:
            try:
                money = float(input("Insert money ($): "))
                if money >= item.price:
                    change = money - item.price
                    print(f"Dispensing {item.name}. Change: ${change:.2f}")
                    item.stock -= 1 # updates stock
                    self.update_slot(item)
                    self.show_dispensing(item.name)
                    break
                else:
                    print("Insufficient funds. Please insert more money.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def update_slot(self, item): # Updates the item slot on the turtle graphics by dislaying "sold out"
        code = [k for k, v in self.items.items() if v == item][0]
        x, y = self.slot_positions[code]
        pen = turtle.Turtle()
        pen.hideturtle()
        pen.penup()
        pen.goto(x + 20, y - 40)
        pen.color("red")
        pen.write("Sold Out", align="center", font=("Arial", 12, "bold"))

    def show_dispensing(self, item_name): # would dislay and animate using turtle graphics
        screen = turtle.Screen()
        screen.title("Vending Machine")
        screen.bgcolor("white")

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(1)

        pen.penup()
        pen.goto(-150, 200)
        pen.pendown()
        pen.color("black")
        pen.begin_fill()
        for _ in range(2):
            pen.forward(300)
            pen.right(90)
            pen.forward(400)
            pen.right(90)
        pen.end_fill()

        y_start = 150
        slot_positions = ["A1", "A2", "B1", "B2", "C1", "C2"]
        index = 0
        for row in range(3):
            for col in range(2):
                x = -120 + (col * 120)
                y = y_start - (row * 120)
                pen.penup()
                pen.goto(x, y)
                pen.pendown()
                pen.color("gray")
                pen.begin_fill()
                for _ in range(2):
                    pen.forward(100)
                    pen.right(90)
                    pen.forward(80)
                    pen.right(90)
                pen.end_fill()

                pen.penup()
                pen.goto(x + 20, y - 40)
                pen.color("black")
                pen.write(slot_positions[index], align="center", font=("Arial", 12, "bold"))
                index += 1

        pen.penup()
        pen.goto(0, -200)
        pen.color("blue")
        pen.write(f"Dispensing {item_name}...", align="center", font=("Arial", 16, "bold"))

        screen.mainloop()

    def admin_mode(self): # added admin, to restock and check inventory
        password = "ilovecybersecurity" # added a password, so only authorized people can access
        attempt = input("Enter admin password: ")
        if attempt == password:
            print("Admin Mode Enabled!")
            while True:
                action = input("Choose an action: (restock/view inventory/exit): ").lower()
                if action == "restock":
                    self.restock_items()
                elif action == "view inventory":
                    self.view_inventory()
                elif action == "exit":
                    print("Exiting Admin Mode.")
                    break
                else:
                    print("Invalid action. Try again.")
        else:
            print("Invalid password.")

    def restock_items(self): # restock items to its max limit which is 10
        for code, item in self.items.items():
            item.stock = 10
        print("All items have been restocked.")

    def view_inventory(self): # check how much is left
        print("Current Inventory:")
        for code, item in self.items.items():
            print(f"{code}: {item.name} - {item.stock} in stock")

    def run(self):
        while True:
            mode = input("Choose mode: (user/admin): ").lower()
            if mode == "user":
                while True:
                    self.display_menu()
                    code = self.select_item()
                    item = self.items[code]
                    self.process_payment(item)

                    another = input("Do you want to buy another item? (yes/no): ").lower()
                    if another != "yes":
                        print("Thank you for using the Vending Machine! Goodbye!")
                        break
            elif mode == "admin":
                self.admin_mode()
            else:
                print("Invalid mode. Try again.")

if __name__ == "__main__": # start of the program, will run a loop
    vending_machine = VendingMachine()
    vending_machine.run()

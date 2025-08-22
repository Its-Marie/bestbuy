# main.py
import products
import store

# setup initial stock of inventory
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
]
best_buy = store.Store(product_list)

def main():
    start(best_buy)

def start(store_obj: store.Store):
    """Start the store menu interface."""
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ").strip()

        if choice == "1":
            # List active products
            products_list = store_obj.get_all_products()
            print("------")
            for idx, p in enumerate(products_list, start=1):
                price_str = f"${p._price:g}"  # formatting like the demo
                print(f"{idx}. {p._name}, Price: {price_str}, Quantity: {p.get_quantity()}")
            print("------")

        elif choice == "2":
            # Show total amount
            total_qty = store_obj.get_total_quantity()
            print(f"Total of {total_qty} items in store")

        elif choice == "3":
            # Make an order
            shopping_list = []
            products_list = store_obj.get_all_products()
            print("------")
            for idx, p in enumerate(products_list, start=1):
                print(f"{idx}. {p._name}, Price: ${p._price:g}, Quantity: {p.get_quantity()}")
            print("------")

            while True:
                prod_input = input("Which product # do you want? ").strip()
                if prod_input == "":
                    break  # finish ordering
                try:
                    prod_idx = int(prod_input) - 1
                    if prod_idx < 0 or prod_idx >= len(products_list):
                        print("Invalid product number. Try again!")
                        continue

                    qty_input = input("What amount do you want? ").strip()
                    if not qty_input.isdigit():
                        print("Quantity must be a positive number.")
                        continue
                    qty = int(qty_input)
                    if qty <= 0:
                        print("Quantity must be greater than zero.")
                        continue

                    shopping_list.append((products_list[prod_idx], qty))
                    print("Product added to list!")

                except ValueError:
                    print("Invalid input. Try again!")

            if shopping_list:
                try:
                    total_payment = store_obj.order(shopping_list)
                    print("********")
                    print(f"Order made! Total payment: ${total_payment:g}")
                except Exception as e:
                    print(f"Error making order: {e}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Error with your choice! Try again!")


if __name__ == "__main__":
    main()

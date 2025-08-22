class Product:
    """
    Represents a product (e.g., 'MacBook Air M2')
    with name, price, quantity, and active status.
    """

    def __init__(self, name: str, price: float, quantity: int):
        # Validation
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        self._name = name.strip()
        self._price = float(price)
        self._quantity = int(quantity)
        # By default, product is active when created
        self._active = True

    # --- Getters/Setters & Status ---
    def get_quantity(self) -> int:
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        self._quantity = quantity
        if self._quantity == 0:
            self._active = False  # Deactivate product if quantity reaches 0

    def is_active(self) -> bool:
        return self._active

    def activate(self) -> None:
        self._active = True

    def deactivate(self) -> None:
        self._active = False

    # --- Display ---
    def show(self) -> None:
        # Display price without unnecessary decimals
        price_str = f"{self._price:g}"
        print(f"{self._name}, Price: {price_str}, Quantity: {self._quantity}")

    # --- Purchase Logic ---
    def buy(self, quantity: int) -> float:
        """
        Buys a given quantity of the product and returns the total price.
        Updates the product's quantity and deactivates it if it reaches 0.
        Raises an Exception if the product is inactive, quantity is invalid,
        or if there is not enough stock.
        """
        if not self._active:
            raise Exception("Product is not active.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a positive integer.")
        if quantity > self._quantity:
            raise Exception("Not enough quantity in stock.")

        total_price = quantity * self._price
        self._quantity -= quantity
        if self._quantity == 0:
            self._active = False
        return float(total_price)


# --- Manual testing (only runs if file is executed directly) ---
if __name__ == "__main__":
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))      # -> 12500.0
    print(mac.buy(100))      # -> 145000.0
    print(mac.is_active())   # -> False (quantity reached 0)

    bose.show()              # "Bose QuietComfort Earbuds, Price: 250, Quantity: 450"
    mac.show()               # "MacBook Air M2, Price: 1450, Quantity: 0"

    bose.set_quantity(1000)
    bose.show()              # "..., Quantity: 1000"

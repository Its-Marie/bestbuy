# store.py
from typing import List, Tuple
import products  # to use products.Product as in the exercise snippet

class Store:
    """Holds a collection of Product instances and supports multi-item orders."""

    def __init__(self, products_list: List["products.Product"]):
        # Keep only valid Product instances
        if not isinstance(products_list, list):
            raise TypeError("products_list must be a list.")
        for p in products_list:
            if not isinstance(p, products.Product):
                raise TypeError("All items in products_list must be Product instances.")
        # Make a shallow copy to avoid accidental outside mutation
        self._products: List[products.Product] = list(products_list)

    def add_product(self, product: "products.Product") -> None:
        """Add a Product to the store."""
        if not isinstance(product, products.Product):
            raise TypeError("product must be a Product instance.")
        self._products.append(product)

    def remove_product(self, product: "products.Product") -> None:
        """Remove a Product from the store."""
        # remove raises ValueError if product not found; let it propagate (clear feedback)
        self._products.remove(product)

    def get_total_quantity(self) -> int:
        """Return total number of items available (only active products counted)."""
        return sum(p.get_quantity() for p in self._products if p.is_active())

    def get_all_products(self) -> List["products.Product"]:
        """Return a list of all active products in the store."""
        return [p for p in self._products if p.is_active()]

    def order(self, shopping_list: List[Tuple["products.Product", int]]) -> float:
        """
        Receive a list of (Product, quantity) tuples, validate, then execute the purchase.
        Returns the total price of the order.

        Strategy:
          1) Validate all items first (so the order is atomic).
          2) If all checks pass, perform the buys and sum the returned prices.
        """
        if not isinstance(shopping_list, list):
            raise TypeError("shopping_list must be a list of (Product, int) tuples.")

        # --- Phase 1: Validate everything (no stock changes yet) ---
        for item in shopping_list:
            if (not isinstance(item, tuple)) or len(item) != 2:
                raise ValueError("Each shopping_list item must be a (Product, int) tuple.")
            prod, qty = item
            if not isinstance(prod, products.Product):
                raise TypeError("First element must be a Product instance.")
            if not isinstance(qty, int) or qty <= 0:
                raise ValueError("Quantity must be a positive integer.")
            if prod not in self._products:
                raise ValueError("Product is not in this store.")
            if not prod.is_active():
                raise ValueError(f"Product '{prod._name}' is not active.")
            if qty > prod.get_quantity():
                raise ValueError(f"Not enough stock for '{prod._name}'.")

        # --- Phase 2: Execute purchases ---
        total_cost = 0.0
        for prod, qty in shopping_list:
            total_cost += prod.buy(qty)  # this updates quantities and may deactivate at 0

        return float(total_cost)


# --- Manual testing (only runs if this file is executed directly) ---
if __name__ == "__main__":
    # Using the exact style from the exercise snippet:
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)

    # Avoid overshadowing the 'products' module in real code,
    # but this mirrors the exercise example closely:
    active_products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(active_products[0], 1), (active_products[1], 2)]))

# Implement Product and ShoppingCart classes to pass the tests

class Product:
    def __init__(self, name: str, price: float):
        # Implement
        pass


class ShoppingCart:
    def __init__(self):
        # Implement
        pass

    def item_count(self) -> int:
        # Implement
        pass

    def total(self) -> float:
        # Implement
        pass

    def add_item(self, product: Product, quantity: int):
        # Implement
        pass

    def remove_item(self, product: Product, quantity: int):
        # Implement
        pass

    def apply_discount(self, percentage: float = None, amount: float = None):
        # Implement
        pass

    def set_tax_rate(self, rate: float):
        # Implement
        pass

    def subtotal(self) -> float:
        # Implement
        pass

    def tax(self) -> float:
        # Implement
        pass

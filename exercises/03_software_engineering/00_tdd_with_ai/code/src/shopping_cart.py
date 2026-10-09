# Implement Product and ShoppingCart classes to pass the tests
"""Shopping cart - the implementation grown test-first in the TDD exercise.

Every method below is an intentionally empty stub: filling them in until the
tests pass IS the exercise. The type checker is therefore told not to
object to the missing return statements here.
"""
# pyrefly: ignore-errors[bad-return]



class Product:
    def __init__(self, name: str, price: float):
        # Implement
        ...


class ShoppingCart:
    def __init__(self):
        # Implement
        ...

    def item_count(self) -> int:
        # Implement
        return 0

    def total(self) -> float:
        # Implement
        return 0.0

    def add_item(self, product: Product, quantity: int):
        # Implement
        ...

    def remove_item(self, product: Product, quantity: int):
        # Implement
        ...

    def apply_discount(self, percentage: float | None = None, amount: float | None = None):
        # Implement
        ...

    def set_tax_rate(self, rate: float):
        # Implement
        ...

    def subtotal(self) -> float:
        # Implement
        return 0.0

    def tax(self) -> float:
        # Implement
        return 0.0

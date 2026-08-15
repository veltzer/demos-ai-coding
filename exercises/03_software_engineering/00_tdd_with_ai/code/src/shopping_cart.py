# Implement Product and ShoppingCart classes to pass the tests
"""Shopping cart - the implementation grown test-first in the TDD exercise.

Every method below is an intentionally empty stub: filling them in until the
tests pass IS the exercise. mypy is therefore told not to object to the
missing return statements here.
"""
# mypy: disable-error-code="empty-body"



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

    def apply_discount(self, percentage: float | None = None, amount: float | None = None):
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

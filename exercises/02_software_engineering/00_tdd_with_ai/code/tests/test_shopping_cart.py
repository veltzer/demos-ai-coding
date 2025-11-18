import pytest
from src.shopping_cart import ShoppingCart, Product

class TestShoppingCart:
    def setup_method(self):
        self.cart = ShoppingCart()
        self.product1 = Product("Widget", 10.00)
        self.product2 = Product("Gadget", 20.00)

    def test_new_cart_is_empty(self):
        """New cart should have zero items."""
        assert self.cart.item_count() == 0
        assert self.cart.total() == 0.0

    def test_add_single_item(self):
        """Adding an item should increase count and total."""
        self.cart.add_item(self.product1, quantity=1)

        assert self.cart.item_count() == 1
        assert self.cart.total() == 10.00

    def test_add_multiple_items(self):
        """Adding multiple items should accumulate."""
        self.cart.add_item(self.product1, quantity=2)
        self.cart.add_item(self.product2, quantity=1)

        assert self.cart.item_count() == 3
        assert self.cart.total() == 40.00

    def test_add_same_item_twice_combines_quantity(self):
        """Adding same item twice should combine quantities."""
        self.cart.add_item(self.product1, quantity=1)
        self.cart.add_item(self.product1, quantity=2)

        assert self.cart.item_count() == 3
        assert self.cart.total() == 30.00

    def test_remove_item_completely(self):
        """Removing all quantity of an item should remove it from cart."""
        self.cart.add_item(self.product1, quantity=2)
        self.cart.remove_item(self.product1, quantity=2)

        assert self.cart.item_count() == 0
        assert self.cart.total() == 0.0

    def test_remove_partial_quantity(self):
        """Removing partial quantity should reduce count."""
        self.cart.add_item(self.product1, quantity=5)
        self.cart.remove_item(self.product1, quantity=2)

        assert self.cart.item_count() == 3
        assert self.cart.total() == 30.00

    def test_remove_item_not_in_cart_raises_error(self):
        """Removing item not in cart should raise error."""
        with pytest.raises(ValueError, match="Product not in cart"):
            self.cart.remove_item(self.product1, quantity=1)

    def test_remove_more_than_available_raises_error(self):
        """Removing more quantity than available should raise error."""
        self.cart.add_item(self.product1, quantity=2)

        with pytest.raises(ValueError, match="Not enough quantity"):
            self.cart.remove_item(self.product1, quantity=3)

    def test_apply_percentage_discount(self):
        """Apply percentage discount to total."""
        self.cart.add_item(self.product1, quantity=2)  # $20
        self.cart.apply_discount(percentage=10)

        assert self.cart.total() == 18.00

    def test_apply_fixed_discount(self):
        """Apply fixed amount discount."""
        self.cart.add_item(self.product1, quantity=2)  # $20
        self.cart.apply_discount(amount=5.00)

        assert self.cart.total() == 15.00

    def test_discount_cannot_make_total_negative(self):
        """Discount should not make total negative."""
        self.cart.add_item(self.product1, quantity=1)  # $10
        self.cart.apply_discount(amount=20.00)

        assert self.cart.total() == 0.00

    def test_only_one_discount_allowed(self):
        """Applying second discount should replace first."""
        self.cart.add_item(self.product1, quantity=2)  # $20
        self.cart.apply_discount(percentage=10)  # $18
        self.cart.apply_discount(percentage=20)  # Should be 20% of $20, not $18

        assert self.cart.total() == 16.00

    def test_calculate_tax(self):
        """Calculate tax on cart total."""
        self.cart.add_item(self.product1, quantity=2)  # $20
        self.cart.set_tax_rate(0.08)  # 8% tax

        assert self.cart.subtotal() == 20.00
        assert self.cart.tax() == 1.60
        assert self.cart.total() == 21.60

    def test_tax_applied_after_discount(self):
        """Tax should be calculated on discounted total."""
        self.cart.add_item(self.product1, quantity=2)  # $20
        self.cart.apply_discount(percentage=10)  # $18
        self.cart.set_tax_rate(0.08)  # 8% tax

        assert self.cart.subtotal() == 18.00
        assert self.cart.tax() == 1.44
        assert self.cart.total() == 19.44

# Implement Product and ShoppingCart to make tests pass

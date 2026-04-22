import unittest
from cart import ShoppingCart

class TestGetTotal(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart_total_is_zero(self):
        self.assertEqual(self.cart.get_total(), 0.0)


class TestApplyDiscount(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("Acer", 2.0, 5)    
        self.cart.add_item("Nitro", 50.0, 1)  

    def test_save10_applied_correctly(self):
        self.cart.apply_discount("SAVE10")
        self.assertEqual(self.cart.get_total(), 54.0)

    def test_save20_applied_correctly(self):
        self.cart.apply_discount("SAVE20")
        self.assertEqual(self.cart.get_total(), 48.0)

    def test_flat5_applied_correctly(self):
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 55.0)

    def test_invalid_code_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.cart.apply_discount("FAKECODE")


class TestAddItem(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_single_item_correct_total(self):
        self.cart.add_item("Book", 15.0, 2)
        self.assertEqual(self.cart.get_total(), 30.0)

    def test_add_multiple_different_items(self):
        self.cart.add_item("Pen", 1.0, 3)
        self.cart.add_item("Notebook", 5.0, 2)
        self.assertEqual(self.cart.get_total(), 13.0)

    def test_add_item_zero_price_allowed(self):
        self.cart.add_item("Gift", 0.0, 1)
        self.assertEqual(self.cart.get_total(), 0.0)


class TestClear(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_clear_empties_cart(self):
        self.cart.add_item("Pen", 2.0, 5)
        self.cart.clear()
        self.assertEqual(self.cart.get_total(), 0.0)

class TestRemoveItem(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_remove_existing_item(self):
        self.cart.add_item("Pen", 2.0, 1)
        self.cart.remove_item("Pen")
        self.assertEqual(self.cart.get_total(), 0.0)


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Pen", 2.0, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Pen", 2.0, -3)



class TestCumulativeState(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_same_item_twice_updates_quantity(self):
        """BUG: uses = instead of +=. qty=2 then qty=3 → should be 5 ($10), gets 3 ($6)."""
        self.cart.add_item("Apple", 2.0, 2)
        self.cart.add_item("Apple", 2.0, 3)
        self.assertEqual(self.cart.get_total(), 10.0)

    def test_add_two_different_items_independent(self):
        self.cart.add_item("A", 5.0, 2)
        self.cart.add_item("B", 3.0, 1)
        self.assertEqual(self.cart.get_total(), 13.0)


class TestDiscountThreshold(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_flat5_exactly_at_threshold_should_apply(self):
        """BUG: uses > instead of >=. Cart of exactly $30 should qualify for FLAT5."""
        self.cart.add_item("Item", 30.0, 1)
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 25.0)

    def test_save20_just_below_threshold_rejected(self):
        self.cart.add_item("Item", 49.99, 1)
        with self.assertRaises(ValueError):
            self.cart.apply_discount("SAVE20")

    def test_save20_above_threshold_accepted(self):
        self.cart.add_item("Item", 60.0, 1)
        self.cart.apply_discount("SAVE20")
        self.assertEqual(self.cart.get_total(), 48.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)

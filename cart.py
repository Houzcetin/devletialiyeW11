class ShoppingCart:
    DISCOUNT_CODES = {
        "SAVE10": {"type": "percent", "value": 10,  "min_order": 0.0},
        "SAVE20": {"type": "percent", "value": 20,  "min_order": 50.0},
        "FLAT5":  {"type": "fixed",   "value": 5.0, "min_order": 30.0},
    }

    def __init__(self):
        self._items = {}
        self._discount = None

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if name in self._items:
            self._items[name]["quantity"] += quantity  # FIX 1: += instead of =
        else:
            self._items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str) -> None:
        if name not in self._items:
            raise KeyError(f"Item '{name}' is not in the cart.")
        del self._items[name]

    def apply_discount(self, code: str) -> None:
        if code not in self.DISCOUNT_CODES:
            raise ValueError(f"'{code}' is not a valid discount code.")
        discount = self.DISCOUNT_CODES[code]
        subtotal = self._subtotal()
        if subtotal >= discount["min_order"]:  # FIX 2: >= instead of >
            self._discount = discount
        else:
            raise ValueError(
                f"A minimum order of ${discount['min_order']:.2f} is required "
                f"for code '{code}'. Your current total is ${subtotal:.2f}."
            )

    def get_total(self) -> float:
        subtotal = self._subtotal()
        if self._discount is None:
            return round(subtotal, 2)
        if self._discount["type"] == "percent":
            discount_amount = subtotal * (self._discount["value"] / 100)  # FIX 3: / instead of //
            return round(max(0.0, subtotal - discount_amount), 2)
        else:
            return round(max(0.0, subtotal - self._discount["value"]), 2)

    def clear(self) -> None:
        self._items = {}

    def get_item_count(self) -> int:
        """TDD GREEN: return sum of all quantities."""
        return sum(item["quantity"] for item in self._items.values())

    def _subtotal(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self._items.values())

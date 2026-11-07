import json
import math
import os
import sys
import tempfile
import unittest
import uuid
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG_FILE = os.path.join(HERE, "catalog.json")
ORDERS_FILE = os.path.join(HERE, "orders.json")


class OrderError(Exception):
    pass


class OutOfStockError(OrderError):
    pass


def is_real_number(value):
    return (not isinstance(value, bool)
            and isinstance(value, (int, float))
            and math.isfinite(value))


def check_quantity(quantity):
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("Quantity must be a whole number of at least 1")


class Product:
    def __init__(self, product_id, name, price):
        if not isinstance(product_id, str) or product_id.strip() == "":
            raise ValueError("Product ID cannot be empty")
        if not is_real_number(price) or price < 0:
            raise ValueError("Price must be zero or more")
        self.product_id = product_id.strip()
        self.name = name
        self.price = price


class Inventory:
    def __init__(self):
        self._products = {}
        self._stock = {}

    @classmethod
    def from_json(cls, path):
        try:
            with open(path, "r", encoding="utf-8") as catalog_file:
                items = json.load(catalog_file)
        except json.JSONDecodeError as error:
            raise ValueError("Catalog file is not valid JSON: " + str(error))

        if not isinstance(items, list):
            raise ValueError("Catalog must be a list of products")

        inventory = cls()
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Every catalog entry must be an object")
            product = Product(item.get("id"), item.get("name", ""), item.get("price"))
            inventory.add_product(product, item.get("stock"))
        return inventory

    def add_product(self, product, stock):
        if product.product_id in self._products:
            raise ValueError("Duplicate product ID: " + product.product_id)
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock for " + product.product_id + " must be zero or more")
        self._products[product.product_id] = product
        self._stock[product.product_id] = stock

    def get_product(self, product_id):
        if product_id not in self._products:
            raise OrderError("Unknown product: " + str(product_id))
        return self._products[product_id]

    def stock_of(self, product_id):
        self.get_product(product_id)
        return self._stock[product_id]

    def check_stock(self, cart):
        problems = []
        for product, quantity in cart.items():
            if product.product_id not in self._products:
                raise OrderError("Unknown product: " + product.product_id)
            available = self._stock[product.product_id]
            if quantity > available:
                problems.append(product.product_id + ": wanted " + str(quantity) + ", only " + str(available) + " in stock")
        if problems:
            raise OutOfStockError("Not enough stock - " + "; ".join(problems))

    def take(self, cart):
        for product, quantity in cart.items():
            self._stock[product.product_id] -= quantity

    def snapshot(self):
        return dict(self._stock)

    def restore(self, snapshot):
        self._stock = dict(snapshot)


class Cart:
    def __init__(self):
        self._lines = {}
        self._discount_percent = 0

    def add(self, product, quantity):
        check_quantity(quantity)
        if product.product_id in self._lines:
            old_quantity = self._lines[product.product_id][1]
            self._lines[product.product_id] = (product, old_quantity + quantity)
        else:
            self._lines[product.product_id] = (product, quantity)

    def remove(self, product_id):
        if product_id not in self._lines:
            raise OrderError("Product is not in the cart: " + str(product_id))
        del self._lines[product_id]

    def items(self):
        return list(self._lines.values())

    def is_empty(self):
        return len(self._lines) == 0

    @property
    def discount_percent(self):
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, percent):
        if not is_real_number(percent) or percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100 percent")
        self._discount_percent = percent

    def subtotal(self):
        return round(sum(product.price * quantity for product, quantity in self.items()), 2)

    def discount_amount(self):
        return round(self.subtotal() * self._discount_percent / 100, 2)

    def total(self):
        return round(self.subtotal() - self.discount_amount(), 2)


class Order:
    def __init__(self, cart):
        self.order_id = "ORD-" + uuid.uuid4().hex[:10].upper()
        self.created_at = datetime.now().isoformat(timespec="seconds")
        self.items = [
            {"product_id": product.product_id, "name": product.name,
             "price": product.price, "quantity": quantity}
            for product, quantity in cart.items()
        ]
        self.subtotal = cart.subtotal()
        self.discount_percent = cart.discount_percent
        self.total = cart.total()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "created_at": self.created_at,
            "items": self.items,
            "subtotal": self.subtotal,
            "discount_percent": self.discount_percent,
            "total": self.total,
        }


class OrderStore:
    def __init__(self, path):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as order_file:
            text = order_file.read()
        if text.strip() == "":
            return []
        try:
            orders = json.loads(text)
        except json.JSONDecodeError as error:
            raise OrderError("Order file is not valid JSON, refusing to overwrite it: " + str(error))
        if not isinstance(orders, list):
            raise OrderError("Order file does not contain a list, refusing to overwrite it")
        return orders

    def save(self, order):
        orders = self.load()
        orders.append(order.to_dict())
        temp_path = self.path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as order_file:
            json.dump(orders, order_file, indent=2)
        os.replace(temp_path, self.path)


def place_order(cart, inventory, store):
    if cart.is_empty():
        raise OrderError("The cart is empty")

    inventory.check_stock(cart)
    order = Order(cart)

    before = inventory.snapshot()
    inventory.take(cart)

    try:
        store.save(order)
    except Exception as error:
        inventory.restore(before)
        raise OrderError("Order could not be saved, stock was put back: " + str(error)) from error

    return order


class FailingStore:
    def save(self, order):
        raise OSError("disk is full")


class OrderTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.orders_path = os.path.join(self.folder.name, "orders.json")
        self.store = OrderStore(self.orders_path)

        self.inventory = Inventory()
        self.inventory.add_product(Product("P1", "Keyboard", 100), 5)
        self.inventory.add_product(Product("P2", "Mouse", 40), 10)

    def make_cart(self, product_id, quantity, discount=0):
        cart = Cart()
        cart.add(self.inventory.get_product(product_id), quantity)
        cart.discount_percent = discount
        return cart

    def test_total_with_discount(self):
        cart = self.make_cart("P1", 2, 10)
        self.assertEqual(cart.subtotal(), 200)
        self.assertEqual(cart.total(), 180)

    def test_order_reduces_stock_and_is_saved(self):
        order = place_order(self.make_cart("P1", 2, 10), self.inventory, self.store)
        self.assertEqual(order.total, 180)
        self.assertEqual(self.inventory.stock_of("P1"), 3)
        saved = self.store.load()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["order_id"], order.order_id)

    def test_order_ids_are_unique(self):
        first = place_order(self.make_cart("P2", 1), self.inventory, self.store)
        second = place_order(self.make_cart("P2", 1), self.inventory, self.store)
        self.assertNotEqual(first.order_id, second.order_id)
        self.assertEqual(len(self.store.load()), 2)

    def test_out_of_stock_changes_nothing(self):
        with self.assertRaises(OutOfStockError):
            place_order(self.make_cart("P1", 6), self.inventory, self.store)
        self.assertEqual(self.inventory.stock_of("P1"), 5)
        self.assertEqual(self.store.load(), [])

    def test_all_items_checked_before_stock_changes(self):
        cart = Cart()
        cart.add(self.inventory.get_product("P1"), 2)
        cart.add(self.inventory.get_product("P2"), 99)
        with self.assertRaises(OutOfStockError):
            place_order(cart, self.inventory, self.store)
        self.assertEqual(self.inventory.stock_of("P1"), 5)
        self.assertEqual(self.inventory.stock_of("P2"), 10)

    def test_invalid_quantities_are_rejected(self):
        cart = Cart()
        product = self.inventory.get_product("P1")
        for bad in (0, -1, 2.5, "3", True, None):
            with self.assertRaises(ValueError):
                cart.add(product, bad)
        self.assertTrue(cart.is_empty())

    def test_invalid_discount_is_rejected(self):
        cart = self.make_cart("P1", 1)
        for bad in (-5, 101, "ten", None):
            with self.assertRaises(ValueError):
                cart.discount_percent = bad

    def test_stock_is_restored_when_saving_fails(self):
        with self.assertRaises(OrderError):
            place_order(self.make_cart("P1", 2), self.inventory, FailingStore())
        self.assertEqual(self.inventory.stock_of("P1"), 5)

    def test_empty_cart_is_rejected(self):
        with self.assertRaises(OrderError):
            place_order(Cart(), self.inventory, self.store)

    def test_corrupt_order_file_is_not_overwritten(self):
        with open(self.orders_path, "w", encoding="utf-8") as order_file:
            order_file.write("{broken")
        with self.assertRaises(OrderError):
            place_order(self.make_cart("P1", 1), self.inventory, self.store)
        with open(self.orders_path, "r", encoding="utf-8") as order_file:
            self.assertEqual(order_file.read(), "{broken")
        self.assertEqual(self.inventory.stock_of("P1"), 5)


def create_sample_catalog(path):
    catalog = [
        {"id": "P1", "name": "Keyboard", "price": 100, "stock": 5},
        {"id": "P2", "name": "Mouse", "price": 40, "stock": 10},
        {"id": "P3", "name": "Monitor", "price": 250, "stock": 2},
    ]
    with open(path, "w", encoding="utf-8") as catalog_file:
        json.dump(catalog, catalog_file, indent=2)


def demo():
    create_sample_catalog(CATALOG_FILE)
    with open(ORDERS_FILE, "w", encoding="utf-8") as order_file:
        order_file.write("[]")

    inventory = Inventory.from_json(CATALOG_FILE)
    store = OrderStore(ORDERS_FILE)

    cart = Cart()
    cart.add(inventory.get_product("P1"), 2)
    cart.discount_percent = 10
    print("Cart 1: P1 x2 with 10% discount, total", cart.total())
    order = place_order(cart, inventory, store)
    print("Placed", order.order_id, "| P1 stock is now", inventory.stock_of("P1"))

    print()
    cart = Cart()
    cart.add(inventory.get_product("P3"), 3)
    print("Cart 2: P3 x3")
    try:
        place_order(cart, inventory, store)
    except OutOfStockError as error:
        print("Rejected:", error)
    print("P3 stock is still", inventory.stock_of("P3"))

    print()
    cart = Cart()
    cart.add(inventory.get_product("P2"), 4)
    cart.add(inventory.get_product("P3"), 1)
    cart.discount_percent = 5
    print("Cart 3: P2 x4 and P3 x1 with 5% discount, total", cart.total())
    order = place_order(cart, inventory, store)
    print("Placed", order.order_id)

    print()
    print("Stock now:", {pid: inventory.stock_of(pid) for pid in ("P1", "P2", "P3")})
    print("Orders saved in orders.json:", len(store.load()))

    print()
    try:
        cart.add(inventory.get_product("P1"), 0)
    except ValueError as error:
        print("Bad quantity:", error)
    try:
        place_order(Cart(), inventory, store)
    except OrderError as error:
        print("Empty cart:", error)
    try:
        inventory.get_product("P99")
    except OrderError as error:
        print("Unknown product:", error)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        demo()

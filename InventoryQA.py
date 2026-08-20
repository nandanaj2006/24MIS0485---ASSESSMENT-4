import unittest
from concurrent.futures import ThreadPoolExecutor
from InventoryManagement import InventoryManagement

class TestInventoryQA(unittest.TestCase):
    def setUp(self):
        self.inv = InventoryManagement()
        self.inv.add_product("Warehouse A", "Laptop", 50)
        self.inv.add_product("Warehouse B", "Laptop", 5)

    def test_stock_availability(self):
        wh = self.inv.select_warehouse_for_order("Laptop", 20)
        self.assertEqual(wh, "Warehouse A")

    def test_insufficient_inventory(self):
        success, msg = self.inv.remove_product("Warehouse B", "Laptop", 10)
        self.assertFalse(success)
        self.assertEqual(msg, "Insufficient inventory.")

    def test_warehouse_transfer(self):
        success, _ = self.inv.transfer_stock("Warehouse A", "Warehouse C", "Laptop", 10)
        self.assertTrue(success)
        self.assertEqual(self.inv.warehouses["Warehouse C"]["Laptop"], 10)

    def test_reorder_threshold(self):
        low = self.inv.check_low_stock()
        self.assertIn(("Warehouse B", "Laptop"), low)

    def test_negative_inventory(self):
        success, _ = self.inv.add_product("Warehouse A", "Laptop", -10)
        self.assertFalse(success)

    def test_invalid_warehouse(self):
        success, msg = self.inv.add_product("Warehouse Z", "Laptop", 10)
        self.assertFalse(success)

    def test_concurrent_orders(self):
        def place_order(qty):
            wh = self.inv.select_warehouse_for_order("Laptop", qty)
            if wh:
                return self.inv.remove_product(wh, "Laptop", qty)
            return False, "None"
        with ThreadPoolExecutor(max_workers=3) as executor:
            res = list(executor.map(place_order, [15, 15, 15]))
        self.assertTrue(any(r[0] for r in res))

if __name__ == "__main__":
    unittest.main()

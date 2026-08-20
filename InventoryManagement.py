class InventoryManagement:
    def __init__(self):
        self.warehouses = {"Warehouse A": {}, "Warehouse B": {}, "Warehouse C": {}}
        self.reorder_threshold = 10
        self.suppliers = {}

    def add_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            return False, "Invalid warehouse."
        if quantity <= 0:
            return False, "Quantity must be greater than zero."
        self.warehouses[warehouse][product] = self.warehouses[warehouse].get(product, 0) + quantity
        return True, f"Added {quantity} of {product} to {warehouse}."

    def remove_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            return False, "Invalid warehouse."
        if quantity <= 0:
            return False, "Quantity must be greater than zero."
        if self.warehouses[warehouse].get(product, 0) < quantity:
            return False, "Insufficient inventory."
        self.warehouses[warehouse][product] -= quantity
        return True, f"Removed {quantity} of {product} from {warehouse}."

    def transfer_stock(self, from_wh, to_wh, product, quantity):
        if from_wh not in self.warehouses or to_wh not in self.warehouses:
            return False, "Invalid warehouse specified."
        success, msg = self.remove_product(from_wh, product, quantity)
        if not success:
            return False, f"Transfer failed: {msg}"
        self.add_product(to_wh, product, quantity)
        return True, f"Transferred {quantity} {product} from {from_wh} to {to_wh}."

    def select_warehouse_for_order(self, product, quantity):
        for wh, items in self.warehouses.items():
            if items.get(product, 0) >= quantity:
                return wh
        return None

    def check_low_stock(self):
        low_stock = {}
        for wh, items in self.warehouses.items():
            for p, qty in items.items():
                if qty <= self.reorder_threshold:
                    low_stock[(wh, p)] = qty
        return low_stock

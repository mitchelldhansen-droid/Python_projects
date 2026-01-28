from data.item_stats import STARTING_INVENTORY


class Inventory:
    def __init__(self):
        self.items = STARTING_INVENTORY.copy()

    def add_item(self, item, quantity=1):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item, quantity=1):
        if item in self.items and self.items[item] >= quantity:
            self.items[item] -= quantity
        else:
            raise ValueError(f"Not enough {item} in inventory")

    def has_item(self, item):
        return self.items.get(item, 0) > 0

    def get_item_count(self, item):
        return self.items.get(item, 0)

    def display_inventory(self):
        print(self.items.copy())

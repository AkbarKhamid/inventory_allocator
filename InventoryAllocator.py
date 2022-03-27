""" 
  My submission for FreeD coding assessment
  File contains python3.9 features for type hinting, it may not work properly on older versions
"""
from typing import Dict, List, TypedDict

OrderType = Dict[str, int]
InventroyType = TypedDict("InventroyType", {"name": str, "inventory": OrderType})
AllocatedType = Dict[str, OrderType]

order = {"apple": 10, "banana": 5}
inventory = [
    {"name": "owd", "inventory": {"apple": 5, "banana": 2}},
    {"name": "dm", "inventory": {"apple": 2, "banana": 2}},
    {"name": "sm", "inventory": {"apple": 3, "banana": 19}},
]


class InventoryAllocator:
    order = None
    inventory = None
    res = []

    def __init__(self, order: OrderType, inventory: InventroyType) -> None:
        self.order = order
        self.inventory = inventory

    def res_index_get_by_name(self, name: str) -> int:
        """finds index of inventory in self.res by its name

        Args:
            name (str): inventory name

        Returns:
            int: index of inventory. returns -1 if it is not in res
        """
        return next(
            (i for i, item in enumerate(self.res) if list(item.keys())[0] == name),
            -1,
        )

    def allocate(self) -> List[AllocatedType]:
        for k, v in self.order.items():
            allocations = self.find_allocation(item_name=k, item_count=v)
            for item in allocations:
                inv_name = list(item.keys())[0]
                inv_index = self.res_index_get_by_name(name=inv_name)
                # inv already added to res
                if inv_index > -1:
                    self.res[inv_index][inv_name][k] = item[inv_name]
                else:
                    self.res.append({inv_name: {k: item[inv_name]}})
        return self.res

    def find_allocation(self, item_name: str, item_count: int) -> List[OrderType]:
        """finds possible inventory combinations for an order

        Args:
            item_name (str): order item name
            item_count (int): order item count

        Returns:
            List[OrderType]: list of possible combinations
        """
        rem_order_size = item_count
        combinations = []
        for inv in self.inventory:
            stock_size = inv["inventory"].get(item_name, 0)
            if stock_size == 0:
                continue

            # inventory has enough units to fullfill order for this item
            if stock_size >= item_count:
                return [{inv["name"]: item_count}]

            # inv has enough units for fullfill the remaining
            if stock_size >= rem_order_size:
                combinations.append({inv["name"]: rem_order_size})
                rem_order_size -= stock_size
                break

            # inv does not have enough units, split
            else:
                combinations.append({inv["name"]: stock_size})
                rem_order_size -= stock_size

        # if not enough units in all warehouses, no allocations
        if rem_order_size <= 0:
            return combinations
        return []


ia = InventoryAllocator(order=order, inventory=inventory)
print("ORDER: ", order)
print("SAMPLE INVENTORY: ", inventory)
res = ia.allocate()

print("RESULT: ", res)

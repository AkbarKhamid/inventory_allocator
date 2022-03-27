from InventoryAllocator import InventoryAllocator


class TestClass:
    def test_always_fails(self) -> None:
        assert False

    def test_always_passes(self) -> None:
        assert True

    def test_not_enough_inventory(self) -> None:
        """not enough inventory -> no allocations"""

        order = {"apple": 3}
        inventory = [{"name": "owd", "inventory": {"apple": 2}}]

        ia = InventoryAllocator(order=order, inventory=inventory)
        res = ia.allocate()

        # empty list
        assert len(res) == 0

    def test_exact_order_inventory_match(self) -> None:
        """happy Case, exact inventory match"""

        order = {"apple": 1}
        inventory = [{"name": "owd", "inventory": {"apple": 1}}]

        ia = InventoryAllocator(order=order, inventory=inventory)
        res = ia.allocate()

        # input and output order unit matches
        assert order["apple"] == res[0][inventory[0]["name"]]["apple"]
        # inventory matches
        assert inventory[0]["name"] == list(res[0].keys())[0]

    def test_exact_order_inventory_match_multiple_items(self) -> None:
        """happy Case, exact inventory match"""

        order = {"apple": 1, "banana": 3}
        inventory = [{"name": "owd", "inventory": {"apple": 1, "banana": 3}}]

        ia = InventoryAllocator(order=order, inventory=inventory)
        res = ia.allocate()

        # input and output order unit matches
        for k, v in order.items():
            assert v == res[0][inventory[0]["name"]][k]
        # inventory matches
        assert inventory[0]["name"] == list(res[0].keys())[0]

    def test_partial_allocate(self) -> None:
        """Should return items from multiple order items that warehouses have enough of"""

        order = {"apple": 10, "banana": 5}
        inventory = [
            {"name": "owd", "inventory": {"apple": 5, "banana": 2}},
            {"name": "dm", "inventory": {"apple": 1, "banana": 2}},
            {"name": "sm", "inventory": {"apple": 2, "banana": 1}},
        ]

        ia = InventoryAllocator(order=order, inventory=inventory)
        res = ia.allocate()

        total_units = 0
        apple_in_res = False
        for item in res:
            print("res", item)
            inv_name = list(item.keys())[0]
            total_units += item[inv_name]["banana"]

            apple_in_res = "apple" in item[inv_name]

        # sum of units should match order
        assert order["banana"] == total_units

        # 'apple' should not be in res
        assert apple_in_res is False

        # no. inventories should match
        assert len(inventory) == len(res)

    def test_should_split_order(self) -> None:
        """Should split an item across warehouses if that is the only way to completely ship an item"""

        order = {"apple": 10}
        inventory = [
            {"name": "owd", "inventory": {"apple": 5}},
            {"name": "dm", "inventory": {"apple": 2}},
            {"name": "sm", "inventory": {"apple": 3}},
        ]

        ia = InventoryAllocator(order=order, inventory=inventory)
        res = ia.allocate()

        total_units = 0
        for item in res:
            inv_name = list(item.keys())[0]
            total_units += item[inv_name]["apple"]

        # sum of units from all warehouses should match order
        assert order["apple"] == total_units

        # no. inventories should match
        assert len(inventory) == len(res)

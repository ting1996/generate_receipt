from libs.receipt import Receipt
import yaml
import os
import random
import copy
import tempfile
from datetime import datetime, timedelta
import re

class RestaurantReceipt(Receipt):
    MAIN_WEIGHT = 3
    SIDE_WEIGHT = 2
    DRINK_WEIGHT = 1
    UPPER_PRICE_RATIO = 0.2
    LOWER_PRICE_DEF = 0

    TAX_RATIO_DEF = 0.08

    DATE_KEY = r"{date}"
    TIME_IN_KEY = r"{time_in}"
    TIME_OUT_KEY = r"{time_out}"

    ITEM_KEY = r"{item}"
    NAME_KEY = r"{name}"
    QUANLITY_KEY = r"{quantity}"
    UNIT_PRICE_KEY = r"{unit_price}"
    TAX_PERCENT_KEY = r"{tax_percent}"
    ITEM_TOTAL_KEY = r"{item_total}"

    TOTAL_KEY = r"{total}"
    TOTAL_QUANTITY_KEY = r"{total_quantity}"
    TOTAL_TAX_KEY = r"{total_tax}"
    TOTAL_WO_TAX_KEY = r"{total_wo_tax}"

    BREAKFAST = 0
    LUNCH = 1
    DINNER = 2

    def __init__(self, path):
        super().__init__(path)
        with open(self.path) as stream:
            self.data = yaml.safe_load(stream)
        self.path_rep = self.path.replace(".yaml", ".rep")
        self.country = self.data["country"]
        self.main = self.data["menu"]["main"]
        self.side = self.data["menu"]["side"]
        self.drink = self.data["menu"]["drink"]
        self.tax = self.data["tax"]
        if self.tax is False:
            self.TAX_RATIO_DEF = 0
        print(f"{self.country=}")
        if self.country == "vn":
            self.LOWER_PRICE_DEF = 500000
    
    def genereate_receipt_line(self, date: datetime, meal_time = DINNER ,lower_price=0, upper_main=0, upper_side=0, upper_drink=1):
        list_items = self.make_random_receipt(lower_price, upper_main, upper_side, upper_drink)
        fp = open(self.path_rep, "r")
        data = fp.read()
        fp.close()
        
        data = data.replace(self.DATE_KEY, date.strftime("%d/%m/%Y"))

        minute_in = random.randint(0, 59)
        delta_hour_out = random.randint(1, 2)
        minute_out = random.randint(0, 59)
        if meal_time == self.BREAKFAST:
            hour_in = random.randint(6, 8)
        elif meal_time == self.LUNCH:
            hour_in = random.randint(11, 13)
        else:
            hour_in = random.randint(17, 19)
        time_in = f"{str(hour_in).zfill(2)}:{str(minute_in).zfill(2)}"
        time_out = f"{str(hour_in+delta_hour_out).zfill(2)}:{str(minute_out).zfill(2)}"
        data = data.replace(self.TIME_IN_KEY, time_in)
        data = data.replace(self.TIME_OUT_KEY, time_out)

        x = re.search(f"({self.ITEM_KEY}([\\s\\S]+){self.ITEM_KEY})", data)
        list_item_str = []
        for item in list_items:
            item_str = copy.copy(x.group(2))
            item_data = list_items[item]
            item_str = item_str.replace(self.NAME_KEY, item_data["name"])
            item_str = item_str.replace(self.QUANLITY_KEY, str(item_data["quantity"]))
            item_str = item_str.replace(self.UNIT_PRICE_KEY, self.format_price(item_data["price"]))
            item_str = item_str.replace(self.TAX_PERCENT_KEY, f"{self.TAX_RATIO_DEF * 100}%")
            item_str = item_str.replace(self.ITEM_TOTAL_KEY, self.format_price(item_data["price"] * item_data["quantity"]))
            
            list_item_str.append(item_str)

        data = data.replace(x.group(1), "".join(list_item_str))
        total_wo_tax, total_tax, total, total_quantity = self.calculate_total(list_items)
        data = data.replace(self.TOTAL_WO_TAX_KEY, self.format_price(total_wo_tax))
        data = data.replace(self.TOTAL_TAX_KEY, self.format_price(total_tax))
        data = data.replace(self.TOTAL_KEY, self.format_price(total))
        data = data.replace(self.TOTAL_QUANTITY_KEY, str(total_quantity))

        fp = tempfile.NamedTemporaryFile(delete=False)
        print(data)
        fp.write(data.encode())

        fp.close()
        return fp.name

    def format_price(self, amount):
        """
        Format an integer amount into price format.

        Args:
            amount (int): The amount to format.

        Returns:
            str: The formatted price string.
        """
        return f"{amount:,.0f}"

    def calculate_total(self, receipt_list):
        """
        Calculate the total price of all items in the receipt list.

        Args:
            receipt_list (list): A list of items, where each item is a dictionary
                                 containing 'price' and 'quantity'.

        Returns:
            float: The total price of the receipt.
        """
        total_wo_tax = 0
        total_quantity = 0
        for item in receipt_list:
            item_data = receipt_list[item]
            total_wo_tax += item_data["price"] * item_data["quantity"]
            total_quantity += item_data["quantity"]
        total_tax = total_wo_tax * self.TAX_RATIO_DEF
        total = total_wo_tax + total_tax
        return total_wo_tax, total_tax, total, total_quantity

    def make_random_receipt(self, lower_price=0, upper_main=0, upper_side=0, upper_drink=1):
        receipt = {}
        total_price = 0
        total_main = 0
        total_side = 0
        total_drink = 0
        if lower_price == 0:
            lower_price = self.LOWER_PRICE_DEF
        upper_price = lower_price + (lower_price * self.UPPER_PRICE_RATIO)
        try_times = 50
        
        while total_price == 0 or total_price > upper_price:
            receipt = {}
            total_price = 0
            while total_price < lower_price:
                kind_food = random.choices(
                    ["main", "side", "drink"],
                    weights=[self.MAIN_WEIGHT, self.SIDE_WEIGHT, self.DRINK_WEIGHT],
                    k=1
                )[0]
                if kind_food == "main" and upper_main != 0 and total_main >= upper_main:
                    continue
                elif kind_food == "side" and upper_side !=0 and total_side >= upper_side:
                    continue
                elif kind_food == "drink" and upper_drink !=0 and total_drink >= upper_drink:
                    continue
                count = 0
                while count < try_times:
                    count += 1
                    item = random.choice(self.data["menu"][kind_food])
                    if item["price"] + total_price <= upper_price:
                        break
                if count == try_times:
                    continue
                # Add item to receipt with quantity
                item_name = item["name"]
                if item_name in receipt:
                    receipt[item_name]["quantity"] += 1
                else:
                    receipt[item_name] = {
                        "name": item_name,
                        "price": item["price"],
                        "quantity": 1
                    }

                total_price += item["price"]

                if kind_food == "main":
                    total_main += 1
                elif kind_food == "side":
                    total_side += 1
                elif kind_food == "drink":
                    total_drink += 1
                print(f"{total_price=}")
        print(f"{total_price=}")
        return receipt

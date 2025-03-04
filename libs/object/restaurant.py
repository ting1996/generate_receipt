from libs.receipt import Receipt
import yaml
import os
import random
import string

class RestaurantReceipt(Receipt):
    MENU_FILE = "menu.yaml"
    MAIN_WEIGHT = 2
    SIDE_WEIGHT = 2
    DRINK_WEIGHT = 1
    def __init__(self, path):
        super().__init__(path)
        with open(os.path.join(self.path, self.MENU_FILE)) as stream:
            self.data = yaml.safe_load(stream)
        self.main = self.data["main"]
        self.side = self.data["side"]
        self.drink = self.data["drink"]
    
    def make_random_receipt(self, lower_price = 0):
        while
        choice_type = random.choices(["main", "side", "drink"], weights=[self.MAIN_WEIGHT, self.SIDE_WEIGHT, self.DRINK_WEIGHT], k=1)
        choice = [random.choice(self.data[choice_type[i]]) for i in range(3)]

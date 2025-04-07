from abc import ABC, abstractmethod
import os
from libs.object import RestaurantReceipt, TaxiReceipt

class ListReceipt():
    RESTAURANT_PATH = os.path.join("assest", "restaurant")
    TAXI_PATH = os.path.join("assest", "taxi")
    def __init__(self):
        self.list_restaurant = self.create_objects(RestaurantReceipt, self.RESTAURANT_PATH)
        self.list_taxi = self.create_objects(TaxiReceipt, self.TAXI_PATH)

    def create_objects(self, object, path):
        list_res = []
        if not os.path.exists(path):
            return list_res

        for dir in os.listdir(path):
            if os.path.isfile(os.path.join(path, dir)):
                if dir.endswith(".yaml"):
                    list_res.append(object(os.path.join(path, dir)))
        return list_res


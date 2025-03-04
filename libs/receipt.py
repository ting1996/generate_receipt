from abc import ABC, abstractmethod
import os
from itertools import combinations

class Receipt(ABC):
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = path

    def __combine(self, _list: list, r: int):
        list_res = []
        for i in range(1, r + 1):
            list_res.extend(combinations(_list, i))
        return list_res


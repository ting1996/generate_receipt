
from libs import ListReceipt



test = ListReceipt()

print(f"{test.list_restaurant=}")
print(f"{test.list_taxi=}")
for res in test.list_restaurant:
    print(f"{res.data=}")
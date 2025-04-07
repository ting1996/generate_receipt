
from libs import ListReceipt
from datetime import datetime


test = ListReceipt()

print(f"{test.list_restaurant=}")
print(f"{test.list_taxi=}")
for res in test.list_restaurant:
    print(f"{res.genereate_receipt_line(datetime(2022,10,2))=}")
from unicodedata import category

from shop.Datacontroller import database

# function for getting settings for payments - send_invoice
def get_data_for_payment(category: str) -> dict:
    settings = dict()
    data = database.read_data(category).copy()[0]
    print(data)
    settings["name"] = category[-1]
    settings["cost"] = data[2]
    settings["preview_path"] = data[-1]
    settings["telegram_id"] = data[4]
    settings["file_path"] = data[3]
    return settings



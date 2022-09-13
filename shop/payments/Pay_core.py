from unicodedata import category
from config import file_path, pre_view_path
from shop.Datacontroller import database


# function for getting settings for payments - send_invoice
def get_data_for_payment(category: list) -> dict:
    category_str = "|".join(category)
    settings = dict()
    data = database.read_data(category_str).copy()
    if len(data) == 1:
        data = database.read_data(category_str).copy()[0]
        settings["name"] = category[-1]
        settings["cost"] = data[2]
        settings["preview_path"] = pre_view_path+data[-1]
        settings["telegram_id"] = data[4]
        settings["file_path"] = file_path+data[3]
    else:
        for i, j in enumerate(data):
            if i == 0:
                settings["name"] = category[-1]
                settings["cost"] = j[2]
                settings["preview_path"] = pre_view_path + j[-1]
                settings["telegram_id"] = j[4]
                settings["file_path"] = [file_path + j[3]]
            else:
                settings["file_path"].append(file_path + j[3])
    return settings



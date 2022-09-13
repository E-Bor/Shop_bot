from bot_logger.BotLogger import logger
import json
import os
import platform



class Categories:
    """Class that needed to switch categories from nested dictionary. Nested dictionary load from json file"""

    def __init__(self, name):
        self.dict = self.read_categories_from_json(name)
        logger.info("loaded dict with categories")

    # read categories from json
    def read_categories_from_json(self, name):
        path = os.path.dirname(__file__)+f"\\{name}.json" if platform.system() == "Windows" else os.path.dirname(
            __file__)+f"/{name}.json"
        with open(path, "r") as f:
            return json.load(f)

    # search item with name 'search' in dict
    def view(self, category=[]):
        dic = self.dict.copy()
        cat = category
        for i in cat:
            if dic[i] == "Pay":
                return dic
            dic = dic[i]
        return list(dic.keys())

    # add category
    def add_category(self, new_cat,  category_list=[]):
        dictionary = self.dict
        logger.info("called function to add category")
        if len(category_list) == 0:
            dictionary[new_cat] = {}
        for j, i in enumerate(category_list):
            if j == len(category_list)-1:
                dictionary[i].update({new_cat: {}})
            dictionary = dictionary[i]
        return dictionary

    # add item for sale
    def add_item(self, new_item, category_list=[]):
        logger.info("called function to add item")
        dictionary = self.dict
        for j, i in enumerate(category_list):
            if j == len(category_list)-1:
                dictionary[i].update({new_item: "Pay"})
            dictionary = dictionary[i]
        return dictionary

    # delete item/category
    def del_partition(self, category_list=[]):
        logger.info("called function to del partition")
        dictionary = self.dict
        for j, i in enumerate(category_list):
            if j == len(category_list)-1:
                del dictionary[i]
                return dictionary
            dictionary = dictionary[i]

    # write changes to json
    def apply_changes(self, name):
        logger.info("changes was applied!")
        path = os.path.dirname(__file__) + f"\\{name}.json" if platform.system() == "Windows" else os.path.dirname(
            __file__) + f"/{name}.json"
        with open(path, "w") as f:
            json.dump(self.dict, f)


category_object = Categories("q")





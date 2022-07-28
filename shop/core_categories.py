from bot_logger.BotLogger import logger
import json
import os
import platform

class Categories:
    """Класс который нужен для создания обьекта переключателя категорий, где вложенный список загружается из
    json файла"""

    def __init__(self,name):
        self.dict = self.read_categories_from_json(name)
        logger.info("loaded dict with categories")

    # read categories from json
    def read_categories_from_json(self, name):
        path = os.path.dirname(__file__)+f"\\{name}.json" if platform.system() == "Windows" else os.path.dirname(__file__)+f"/{name}.json"
        with open(path, "r") as f:
            return json.load(f)

    # search item with name 'search' in dict
    def search_categories(self,dict_for_search,search):
        logger.info("Called search element in dictionary")
        if search in dict_for_search.keys():
            return dict_for_search[search]
        for i in dict_for_search.values():
            if isinstance(i,dict):
                new = self.search_categories(i, search)
                if new != None:
                    return new

    # view all items in categories
    def view_category(self,key_for_view="start"):
        if key_for_view == "start":
           return list(self.dict.keys())
        else:
            return self.search_categories(self.dict, key_for_view)

    # view only current items in categories
    def view(self,category = "start"):
        logger.info("Shown categories")
        categories = self.view_category(category)
        if isinstance(categories,dict):
            return list(self.view_category(category).keys())
        return categories


category_object = Categories("q")




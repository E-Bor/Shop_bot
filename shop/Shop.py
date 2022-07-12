import os
import json

import shop as shop


class Shop:
    """class for creating shop
    It creating JSON file with a name of shop in first position, but other positions has ShopObjects`s objects with its names
    """

    def __init__(self,name_of_shop):
        self.__name = name_of_shop
        self.categories = dict()
        self.categories["name"] = name_of_shop

        with open(f"{name_of_shop}.json","w+") as f:
            json.dump(self.create_dict_attrs(),f)

# create dict "dict_attrs" witch attrs for all objects in "categories" list
    def create_dict_attrs(self):
        dict_attrs = dict()
        for i in self.categories:
            if isinstance(self.categories[i],str):
                continue
            dict_attrs[i] = self.categories[i].__dict__
        print(dict_attrs)
        return dict_attrs

# method for creating objects in categories list with dict. dict_attrs must have all information about
# objects`s attributes
    def assembly_objects(self,dict_attrs):
        for i in dict_attrs:
            if i == "name": continue
            a = ShopObjects("","",0)
            a.__dict__ = dict_attrs[i]
            self.categories[i] = a


# Adding new position to Json

    def add_del_new_position(self,object_of_shop,task=True):
        if isinstance(object_of_shop,ShopObjects):
            with open(f"q.json","r") as f:
                a = json.load(f)
                self.assembly_objects(a)
                if task:
                    self.categories[object_of_shop.name] = object_of_shop
                if not task:
                    self.categories.pop(object_of_shop.name,"Object not found")
            with open(f"q.json", "w") as f:
                json.dump(self.create_dict_attrs(), f)
        else:
            print(f"ShopObjects hasn`t '{object_of_shop}', with 'name': {object_of_shop.name}")




class ShopObjects:
    """class that view shop`s sections"""

    def __init__(self,name,discription_object ,price):

        if isinstance(discription_object, str) and isinstance(name, str):
            self.discription_object = discription_object
            self.name = name

        if isinstance(price, int):
            self.price = price

        else:
            self.discription_object = "1"
            self.price = 0

class WorkWithJSON:
    pass


shop1 = Shop("q")
k1 = ShopObjects("qwe","asd",1)
k2 = ShopObjects("qwe2","asd2",12)

# shop1.add_del_new_position(k2,True)
shop1.categories[k1.name] = k1
shop1.create_dict_attrs()
shop1.add_del_new_position(k1,True)
shop1.add_del_new_position(k2,True)
shop1.add_del_new_position(k1,False)

# shop1.assembly_objects({'qwe  ': {'_ShopObjects__discription_object': 'asd', 'name': s'qwe', '_ShopObjects__price': 1}, 'qwe2': {'_ShopObjects__discription_object': 'asd2', 'name': 'qwe2', '_ShopObjects__price': 12}})
shop1.categories


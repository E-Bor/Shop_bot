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
        try:
            with open(f"{name_of_shop}.json","x+") as f:        #Сюда прикрутить функцию чтения параметров из файла
                self.read_shop_from_json()

        except FileExistsError:
            with open(f"{name_of_shop}.json", "w+") as f:
                json.dump(self.create_dict_attrs(), f)


# create dict "dict_attrs" witch attrs for all objects in "categories" list
    def create_dict_attrs(self) -> dict:
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
            with open(f"{self.__name}.json","r") as f:
                self.assembly_objects(json.load(f))
                if task:
                    self.categories[object_of_shop.name] = object_of_shop
                if not task:
                    self.categories.pop(object_of_shop.name,"Object not found")
            with open(f"{self.__name}.json", "w") as f:
                json.dump(self.create_dict_attrs(), f)
        else:
            print(f"ShopObjects hasn`t '{object_of_shop}', with 'name': {object_of_shop.name}")

# functions for read and load Shop object with all attributes from/to json
    def read_shop_from_json(self):
        with open(f"{self.__name}.json", "r") as f:
            self.assembly_objects(json.load(f))

    def load_shop_to_json(self):
        with open(f"{self.__name}.json", "w+") as f:
            json.dump(self.create_dict_attrs(), f)




class ShopObjects:
    """class that view shop`s sections"""

    def __init__(self,name,discription_object ,price):
        self.__name = name                                             # this reauied attributes, that can`t del
        self.__discription_object = discription_object
        self.__price = price
        self.__links_for_next_objects = list()
        self.__link_for_previous_object = None

# setters and gatters for default attributes
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = "Default_name"

    @property
    def discription_object(self):
        return self.__discription_object

    @discription_object.setter
    def discription_object(self,discription_object):
        if isinstance(discription_object, str):
            self.__discription_object = discription_object
        else:
            self.discription_object = "Default_discription"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,price):
        if isinstance(price, int):
            self.__price = price
        else:
            self.__price = 0

    @property
    def links_for_next_objects(self):
        return self.__links_for_next_objects

    @links_for_next_objects.setter
    def links_for_next_objects(self, objects):
        if isinstance(objects, ShopObjects):
            self.__links_for_next_objects.append(objects)

    @links_for_next_objects.deleter
    def links_for_next_objects(self,objects):
        if objects in self.__links_for_next_objects:
            self.__links_for_next_objects.remove(objects)
        else:
            print("links_for_next_objects not found")

    @property
    def link_for_previous_object(self):
        return self.__link_for_previous_object

    @link_for_previous_object.setter
    def link_for_previous_object(self, objects):
        if isinstance(objects, ShopObjects):
            self.__link_for_previous_object = objects

    @link_for_previous_object.deleter
    def link_for_previous_object(self):
        self.__link_for_previous_object = None









shop1 = Shop("q")
k1 = ShopObjects("qwe","asd",1)
k2 = ShopObjects("qwe2","asd2",12)

# shop1.add_del_new_position(k2,True)
shop1.categories[k1.name] = k1
shop1.create_dict_attrs()
shop1.add_del_new_position(k1,True)
shop1.add_del_new_position(k2,True)
shop1.add_del_new_position(k1,False)

# k1.links_for_next_objects = k2
# k1.links_for_next_objects = k2
# print(k1.links_for_next_objects)
# shop1.assembly_objects({'qwe  ': {'_ShopObjects__discription_object': 'asd', 'name': s'qwe', '_ShopObjects__price': 1}, 'qwe2': {'_ShopObjects__discription_object': 'asd2', 'name': 'qwe2', '_ShopObjects__price': 12}})
shop1.categories


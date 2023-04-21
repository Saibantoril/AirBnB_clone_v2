#!/usr/bin/python3
"""File Storage Module"""

import json
import os.path


class FileStorage:
    """Serializes instances to JSON file and deserializes
    JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        json_dict = {}
        for key, value in self.__objects.items():
            json_dict[key] = value.to_dict()
        with open(self.__file_path, mode='w', encoding='utf-8') as file:
            json.dump(json_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, mode='r', encoding='utf-8') as file:
                json_dict = json.load(file)
                for key, value in json_dict.items():
                    cls_name, obj_id = key.split('.')
                    module = __import__("models." + cls_name, fromlist=[cls_name])
                    cls = getattr(module, cls_name)
                    self.__objects[key] = cls(**value)

    def close(self):
        """Deserializes the JSON file to __objects"""
        self.reload()

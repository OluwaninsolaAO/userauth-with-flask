#!/usr/bin/python3
"""Storage"""
import json


class Storage():
    """File Storage class"""
    __objs = {}
    __filedbname = 'data.json'

    def __init__(self):
        pass

    def add(self, obj):
        key = obj.__class__.__name__ + '.' + obj.email
        self.__objs.update({key: obj})

    def save(self):
        with open(self.__filedbname, 'w') as f:
            data = {}
            for key, value in self.__objs.items():
                data.update({key: value.__dict__})
            json.dump(data, f)

    def delete(self, obj):
        self.__objs.pop(obj.__class__.__name__ + '.' + obj.email, None)

    def reload(self):
        from models.user import User
        try:
            with open(self.__filedbname, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        self.__objs = {}
        for key, value in data.items():
            self.__objs.update({key: User(**value)})

    def get(self, cls, id):
        return self.__objs.get(cls.__name__ + '.' + id, None)

    def all(self):
        return self.__objs

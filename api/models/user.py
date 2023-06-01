#!/usr/bin/python3
"""User"""
from models.storage import Storage
from models.utils.hash_password import hash_password

storage = Storage()


class User():
    """User Class"""

    def __init__(self, email, password, **kwargs):
        if kwargs:
            for attr in ['email', 'password']:
                if attr not in kwargs:
                    return
                setattr(self, attr, kwargs.get(attr))
            return
        self.email = email
        self.password = password

    def save(self):
        storage.add(self)
        storage.save()

    def delete(self):
        storage.delete(self)

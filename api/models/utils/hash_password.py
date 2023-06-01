#!/usr/bin/python3
def hash_password(text):
    """Encrypt password"""
    from hashlib import sha256
    return sha256(text.encode()).hexdigest()

import base64
import hashlib
import random
import uuid

def get_salt():
    salt = uuid.uuid4().hex
    return salt

def hash_password(plain_text_pwd, salt):
    hashed_password = hashlib.sha512(plain_text_pwd + salt.encode('utf-8')).hexdigest()
    return hashed_password

def hash_password_256(plain_text_pwd, salt):
    """Assumes plain_text_input is of `bytes` type"""
    return hashlib.sha256(plain_text_pwd.encode('utf-8') + salt.encode('utf-8')).hexdigest()

def check_password(plain_text_input, user_salt, user_password):
    hashed_input = hash_password(plain_text_input, user_salt)
    return hashed_input == user_password # user_password is stored as hash

def create_password(plain_text_pwd):
    salt = get_salt()
    password = hash_password(plain_text_pwd, salt)
    return (salt, password)

def generate_token():
    return str(uuid.uuid4()).replace("-", "")

def get_md5sum(plain_text_input):
    return hashlib.md5(plain_text_input.encode('utf-8')).hexdigest()

def check_md5_password(plain_text_input, user_password_hash):
    md5sum = get_md5sum(plain_text_input)
    return md5sum == user_password_hash
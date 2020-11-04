import json


class User:
    id = 1
    username = "Alex"
    profession = "Driver"
    salary = 200_000

user = User()
"""result = dict(user)
print(result)"""
print(user.__dict__)

json.JSONDecoder()
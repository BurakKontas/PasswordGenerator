from typing import TypedDict
from collections import ChainMap
import random

class Options(TypedDict):
    upper: bool
    lower: bool
    symbol: bool
    number: bool
    length: int
    quantity: int

default_options: Options = {
    "upper": True,
    "lower": True,
    "symbol": True,
    "number": True,
    "length": 10,
    "quantity": 5
}

uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowers = "abcdefghijklmnopqrstuvwxyz"
symbols = "!@#$%^&*()_+-=,./<>?;':\"[]{}\\|`~"
numbers = "0123456789"

values = {
    "upper": uppers, 
    "lower": lowers, 
    "symbol": symbols, 
    "number": numbers
}

def clean_options(options:dict) -> Options: 
    temp_dict = options.copy()
    default_keys = default_options.keys()
    for key in options.keys():
        if key not in default_keys:
            temp_dict.pop(key)
    return temp_dict

class PasswordGenerator:
    def __init__(self, options: Options = default_options) -> None:
        self.options = ChainMap(options, default_options)
        self.options = dict(self.options)
        self.options = clean_options(self.options)
        if not options.get("upper") and not options.get("lower") and not options.get("number") and not options.get("symbol"):
            raise ValueError("At least one of 'upper', 'lower', 'number', or 'symbol' must be True.")
        self.passwords = []
        self.__generate_passwords()

    def __assign_random_value(self, password:list, indexes:list, values:list):
        password = password.copy() 
        for index in indexes:
            replace_value = random.choice(values)
            password[index] = replace_value
        return password

    def __generate_passwords(self):
        for _ in range(self.options.get("quantity")):
            password = [None] * self.options.get("length")
            
            while None in password:
                for key, value in self.options.items():
                    if value and key in ("upper", "lower", "symbol", "number"):
                        indexes = [i for i, item in enumerate(password) if item is None]
                        if not indexes:
                            break
                        n = random.randint(1, min(len(indexes), 5))
                        replace_indexes = random.sample(indexes, n)
                        password = self.__assign_random_value(password, replace_indexes, values[key]) 
                if None not in password:
                    break
            self.passwords.append("".join(password))

    def __str__(self) -> str:
        result = "Passwords:\n"
        for index, password in enumerate(self.passwords):
            result += str(index + 1) + ". " + str(password) + "\n"
        result = result.removesuffix("\n")
        return result
            
pg = PasswordGenerator(options={
    "quantity":10,
    "length":100,
    "upper": True,
    "number": True,
    "symbol": False,
    "lower": True
})

print(pg)
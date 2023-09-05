from typing import TypedDict
from collections import ChainMap
import random

# User experience açıcısından kullanıcı options olarak ne parametre gireceğini bilsin diye bir class
class Options(TypedDict):
    upper: bool
    lower: bool
    symbol: bool
    number: bool
    length: int
    quantity: int

# Default değerleri içeren class eğer classa parametre olarak verilmezse buradaki değer alınacak
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

# Gereksiz keyleri çıkartan fonksiyon 
def clean_options(options:dict) -> Options: 
    temp_dict = options.copy()
    default_keys = default_options.keys()
    for key in options.keys():
        if key not in default_keys:
            temp_dict.pop(key)
    return temp_dict

class PasswordGenerator:
    def __init__(self, options: Options = default_options) -> None:
        self.options = ChainMap(options, default_options) # bu kısım optionsta olmayan değişkenleri default ile değiştiriyor
        self.options = dict(self.options)
        self.options = clean_options(self.options) # buda gereksiz yani default ta olmayan parametreleri siliyor
        if not options.get("upper") and not options.get("lower") and not options.get("number") and not options.get("symbol"):
            raise ValueError("At least one of 'upper', 'lower', 'number', or 'symbol' must be True.") # Hepsi false ise sonsuz döngüye girecek o yüzden hata veriyoz
        self.passwords = []
        self.__generate_passwords()

    # Bu kısım şifredeki verilen indexleri values deki random değerlerle değiştiriyor
    def __assign_random_value(self, password:list, indexes:list, values:list):
        password = password.copy() 
        for index in indexes:
            replace_value = random.choice(values) # Values den random bir seçim yapıyor
            password[index] = replace_value
        return password

    def __generate_passwords(self):
        for _ in range(self.options.get("quantity")):
            password = [None] * self.options.get("length") # [None, None, None, None, ..., None]
            
            while None in password:
                for key, value in self.options.items():
                    if value and key in ("upper", "lower", "symbol", "number"): # eğer value True ise ve key bu yandaki tuple içerisindeyse aşağıdaki if'e giriyor
                        indexes = [i for i, item in enumerate(password) if item is None]
                        if not indexes:
                            break # eğer None yok ise ve burada yakaladıysak döngüyü kırıyoruz
                        n = random.randint(1, min(len(indexes), 5)) # Max 5 adet değiştiriyoruz tek seferde
                        replace_indexes = random.sample(indexes, n) # indexes içerisinden n adet rastgele değer alıyor
                        password = self.__assign_random_value(password, replace_indexes, values[key]) 
                if None not in password:
                    break  # şifre tamamen oluştuysa içerisinde none yok ise kırıyoz artık döngüyü
            self.passwords.append("".join(password)) # En sonda diziyi stringe çevirip passwordsa ekliyoruz

    def __str__(self) -> str: # javadaki toString fonksiyonunun overridesi ile aynı şey bu fonksiyon
        result = "Passwords:\n"
        for index, password in enumerate(self.passwords):
            result += str(index + 1) + ". " + str(password) + "\n"
        result = result.removesuffix("\n") # en sonra fazladan \n koyuyor onu siliyoruz
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
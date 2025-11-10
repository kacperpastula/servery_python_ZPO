from typing import Optional, List, TypeVar
from abc import ABC, abstractmethod
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, _name: str, _price: float):
        if not re.fullmatch('^[a-zA-Z]+\\d+$', _name):
            raise ValueError
        else:
            self.name = _name
            self.price = _price
    def __eq__(self, other):
        return (self.name == other.name) and (self.price == other.price)  # FIXME: zwróć odpowiednią wartość
 
    def __hash__(self):
        return hash((self.name, self.price))
 
class ServerError(Exception):
    pass
class TooManyProductsFoundError:
    
      # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

class Server(ABC):
    n_max_returned_entries: int = 4
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def get_entries(self, n_letters: int = 1) -> list[Product]:
        entries = []
        letters = 0
        numbers = 0
        for n in self.get_all_products(n_letters):
            for c in self.get_all_products(n_letters)[n]:
                if c.isalpha():
                    letters +=1
                elif c.isnumeric():
                    numbers += 1
            if letters == n and (numbers == 2 or numbers == 3):
                entries.append(n)
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError()
        return sorted(entries, key=lambda entry: entry.name)
    @abstractmethod
    def get_all_products(self, n_letters: int = 1) -> list[Product]:
        raise NotImplementedError()
        pass
ServerType = TypeVar('ServerType', bound=Server)
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


    
    
class ListServer(Server):
    def __init__(self, _products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: List[Product] = _products

    def get_all_products(self, n_letters = 1) -> List[Product]:
        return self.products
    pass
 
 
class MapServer:
    def __init__(self, _products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: dict[str, Product] = {p.name for p in _products}

    def get_all_products(self, n_letters = 1) -> List[Product]:
        return list(self.products.values())
        
    pass
 

class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, _server: ServerType) -> None:
        self.server: ServerType = _server

    def get_total_price(self, n_letters: int) -> Optional[float]:
        try:
            entries = self.server.get_entries() if n_letters is None else self.server.get_entries(n_letters)
            if not entries:
                return None
            total_price = sum([p.price for p in entries])
            return total_price
        except TooManyProductsFoundError:
            return None
        pass
from typing import Optional, List, TypeVar, Dict
from abc import ABC, abstractmethod
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, _name: str, _price: float) -> None:
        if not re.fullmatch('^[a-zA-Z]+\\d+$', _name):
            raise ValueError
        else:
            self.name: str = _name
            self.price: float = _price
    def __eq__(self, other) -> bool:
        return isinstance(other, Product) and (self.name == other.name) and (self.price == other.price)  # FIXME: zwróć odpowiednią wartość
 
    def __hash__(self) -> int:
        return hash((self.name, self.price))
 
class ServerError(Exception):
    pass
class TooManyProductsFoundError(ServerError):
    
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

class Server(ABC):
    n_max_returned_entries: int = 4

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: int = 1) -> List[Product]:

        product_code = '^[a-zA-Z]{{{}}}\\d{{2,3}}$'.format(n_letters)
        entries = [p for p in self.get_all_products(n_letters) if re.fullmatch(product_code, p.name)]
        
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(entries, key=lambda entry: entry.price)
    
    @abstractmethod
    def get_all_products(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError
        
ServerType = TypeVar('ServerType', bound=Server)
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


    
    
class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__products: List[Product] = products

    def get_all_products(self, n_letters: int = 1) -> List[Product]:
        return self.__products
    
 
 
class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__products: Dict[str, Product]= {p.name: p for p in products}

    def get_all_products(self, n_letters: int = 1) -> List[Product]:
        return list(self.__products.values())
        
    
 

class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: ServerType) -> None:
        self.server: ServerType = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            entries = self.server.get_entries() if n_letters is None else self.server.get_entries(n_letters)
            if not entries:
                return None
            total_price = sum([entry.price for entry in entries])
            return total_price
        except TooManyProductsFoundError:
            return None
        
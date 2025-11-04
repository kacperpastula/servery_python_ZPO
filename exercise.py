from typing import Optional
from abc import ABC, abstractmethod
class Server(ABC):
    def __init__()
    @abstractmethod 
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, _name: str, _price: float):
        self.name = _name
        self.price = _price
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  # FIXME: zwróć odpowiednią wartość
 
    def __hash__(self):
        return hash((self.name, self.price))
 
 
class TooManyProductsFoundError:
      # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
 
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

    
    
class ListServer:
    def __init__(self, _products: List[Product]):
        self.products = _products
    def get_entries(self, n_letters):
        entries = []
        letters = 0
        numbers = 0
        for n in self.products:
            for c in self.products[n]:
                if c.isalpha():
                    letters +=1
                elif c.isnumeric():
                    numbers += 1
            if letters == n and (numbers == 2 or numbers == 3):
                entries.append(n)
        return entries
    pass
 
 
class MapServer:
    def __init__(self, _products: List[Product]):
        
    pass
 
 
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, _server: )
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()
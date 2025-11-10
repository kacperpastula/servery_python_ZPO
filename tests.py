import unittest
from collections import Counter
 
from exercise import ListServer, Product, Client, MapServer, TooManyProductsFoundError
 
server_types = (ListServer, MapServer)
class ServerSortingTest(unittest.TestCase):
    def test_list_server_returns_sorted_entries(self):
        # tworzymy produkty z pasującymi nazwami, ale w przypadkowej kolejności cen
        products = [
            Product("PP123", 30),
            Product("PP124", 10),
            Product("PP125", 20),
        ]

        server = ListServer(products)
        entries = server.get_entries(2)  # dopasują wszystkie PP + 3 cyfry

        # sprawdzamy czy są posortowane rosnąco po cenie
        prices = [p.price for p in entries]
        self.assertEqual(prices, [10, 20, 30])


class ServerLimitTest(unittest.TestCase):
    def test_too_many_products_raises_exception(self):
        # 5 produktów pasuje do n_letters=2 — a limit to 4
        products = [
            Product("AA10", 1),
            Product("AA11", 2),
            Product("AA12", 3),
            Product("AA13", 4),
            Product("AA14", 5),
        ]

        server = ListServer(products)

        with self.assertRaises(TooManyProductsFoundError):
            server.get_entries(2)


class ClientTotalPriceTest(unittest.TestCase):
    def test_total_price_when_exception_or_no_results(self):
        # przypadek 1: zbyt wiele wyników → klient powinien zwrócić None
        too_many = [
            Product("BB10", 1),
            Product("BB11", 1),
            Product("BB12", 1),
            Product("BB13", 1),
            Product("BB14", 1),
        ]
        server = ListServer(too_many)
        client = Client(server)
        self.assertIsNone(client.get_total_price(2))   # wyjątek → None

        # przypadek 2: brak wyników → również None
        no_match = [Product("CC10", 5)]
        server2 = ListServer(no_match)
        client2 = Client(server2)
        self.assertIsNone(client2.get_total_price(3))   # brak wyników → None

    
 
class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))
 
 
class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
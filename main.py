import unittest
from tests import *


if __name__ == '__main__':
    kc310 = Product("KC310", 199.99)
    sp450 = Product("SP450", 249.99)
    zx81 = Product("ZX81", 49.99)
    products = [kc310, sp450, zx81]
    server = ListServer(products)
    client = Client(server)
    print(f"Total price: {client.get_total_price(2)}")
    
    unittest.main()

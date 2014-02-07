#!/usr/bin/env python
from transaction import Transaction

class Sale(Transaction):
    @staticmethod
    def Process(ean, quantity, time):
        k = ndb.Key('Product', ean)
        product = k.get()

        quantity = int(quantity)

        if product:
            price = product.priceOut
            product.inStock -= quantity
            product.put()
            s = Sale(product=k, quantity=quantity, price=price, time=time)
            s.put()
        else:
            logging.error("SALE COULD NOT GET YOUR BLOODY PRODUCT!")

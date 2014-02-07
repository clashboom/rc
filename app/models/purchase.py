#!/usr/bin/env python
from transaction import Transaction

class Purchase(Transaction):
    @staticmethod
    def Process(ean, price, quantity, description=None, time=None):
        k = ndb.Key('Product', ean)
        product = k.get()

        if product:

            if description:
                product.description = description

            product.priceIn = price
            product.priceOut = price * 1.30
            product.inStock += quantity

        else:

            product = Product(id=ean,
                              description=description,
                              priceIn=price,
                              priceOut=price * 1.30,
                              inStock=quantity)
        product.put()

        purchase = Purchase(product=ndb.Key('Product', ean),
                            quantity=quantity,
                            price=price, time=time)
        purchase.put()

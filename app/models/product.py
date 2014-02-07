#!/usr/bin/env python
class Product(ndb.Model):
    description = ndb.StringProperty('d', required=True)
    priceIn = ndb.FloatProperty('pi', required=True)
    priceOut = ndb.FloatProperty('po', required=True)
    inStock = ndb.FloatProperty('qt', required=True, default=0)
    eka = ndb.StringProperty('eka')

#!/usr/bin/env python
class Transaction(ndb.Model):
    product = ndb.KeyProperty('k', kind='Product')
    quantity = ndb.FloatProperty('qt', required=True, default=1)
    price = ndb.FloatProperty('ppi', required=True)
    time = ndb.DateTimeProperty()
    eka = ndb.StringProperty()

    @classmethod
    def QueryByKey(cls, key, timeRangeFrom=None, timeRangeTo=None):
        if timeRangeFrom:
            if timeRangeTo:
                q = cls.query(cls.product == key,
                              cls.time >= timeRangeFrom,
                              cls.time <= timeRangeTo)
            else:
                q = cls.query(cls.product == key,
                              cls.time >= timeRangeFrom)
        elif timeRangeTo:
            q = cls.query(cls.product == key,
                          cls.time <= timeRangeTo)
        else:
            q = cls.query(cls.product == key)

        return q

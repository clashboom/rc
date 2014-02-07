#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers import *

# My URL mappings
route_list = [
    ('/db', PopulateDB),
    ('/buy', PurchaseHandler),
    # ('/sell(?:/)?(?:([0-9]+)/([0-9]+))?', SalesHandler),
    ('/sell', SalesHandler),
    ('/prece', ProductSingle),
    ('/', MainPage)
]

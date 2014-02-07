# Let's roll
import jinja2
import logging
import os
import random
import webapp2

from google.appengine.ext import ndb
from datetime import datetime, timedelta
from libs import gviz_api

## The word Transaction in this file is used in a commercial context, it has
## nothing to do with database transactions.

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    @classmethod
    def render_str(cls, template, *a, **params):
        template = JINJA_ENV.get_template(template)
        return template.render(params)

    def render(self, template, *a, **params):
        self.write(self.render_str(template, *a, **params))


class MainPage(Handler):
    def get(self):
        logging.error('OHAI FROM MAIN PAGE!')
        self.render('menu.html')


class Product(ndb.Model):
    description = ndb.StringProperty('d', required=True)
    priceIn = ndb.FloatProperty('pi', required=True)
    priceOut = ndb.FloatProperty('po', required=True)
    inStock = ndb.FloatProperty('qt', required=True, default=0)
    eka = ndb.StringProperty('eka')


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

    @classmethod
    def Query(cls, timeRangeFrom=None, timeRangeTo=None):
        """
        OH SPARE ME, THE GODS OF DRY
        """
        if timeRangeFrom:
            if timeRangeTo:
                q = cls.query(cls.time >= timeRangeFrom,
                              cls.time <= timeRangeTo)
            else:
                q = cls.query(cls.time >= timeRangeFrom)
        elif timeRangeTo:
            q = cls.query(cls.time <= timeRangeTo)
        else:
            q = cls.query()

        return q


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


class PurchaseHandler(Handler):
    #TODO: change this to POST
    def get(self):
        ean = self.request.get('ean')
        quantity = float(random.randint(0, 10))
        price = float(self.request.get('p'))
        description = self.request.get('desc')
        Purchase.Process(ean=ean, quantity=quantity, price=price,
                         description=description)
        self.redirect('/')


class SalesHandler(Handler):
    #TODO: change this to POST
    def get(self):
        ean = self.request.get('ean')
        quantity = float(random.randint(0, 10))
        Sale.Process(ean=ean, quantity=quantity)
        self.redirect('/')


class Utilities(Handler):
    @staticmethod
    def translateDates(no=None, lidz=None, periods=None):
        """
        Translates dates from javascript datetimepicker to type datetime.
        Will optionally accept unset range (first 2) args and
        pre-set period argument, which is translated to appropriate date range.
        """
        if no:
            no = datetime.strptime(no, '%Y/%m/%d %H:%M:%S')
        if lidz:
            lidz = datetime.strptime(lidz, '%Y/%m/%d %H:%M:%S')

        if periods:
            now = datetime.now()
            today = datetime(year=now.year, month=now.month, day=now.day)
            if periods == 'sodien':
                no = today
            elif periods == 'vakar':
                no = today - timedelta(days=1)
            elif periods == 'sonedel':
                # no need for -1 because weekdays are 0 indexed
                no = today - timedelta(days=today.weekday())
            elif periods == 'somenes':
                # need -1 here because there is no 0th day of the month
                no = today - timedelta(days=today.day - 1)
            elif periods == 'ieprnedela':
                thisweek = today - timedelta(today.weekday())
                no = thisweek - timedelta(weeks=1)
                lidz = thisweek
            elif periods == 'ieprmenesis':
                monthago = today - timedelta(weeks=4)
                no = monthago - timedelta(days=monthago.day - 1)
                lidz = today - timedelta(days=today.day - 1)
        return (no, lidz)

    @staticmethod
    def getTransactions(no, lidz, key=None):
        """
        getTransactions (datetime_from, datetime_to, key) -> ([x], [y])
        Given an optional entity's key and two datetime types, will query
        transactions - sales and purchases in the given time range and return
        a tuple of lists
        Note: returns a tuple of lists of entities
        """
        purchases = list()
        sales = list()

        if key:
            product = key.get()
            if product:
                purchases = list(Purchase.QueryByKey(key, timeRangeFrom=no,
                                                     timeRangeTo=lidz))
                sales = list(Sale.QueryByKey(key, timeRangeFrom=no,
                                             timeRangeTo=lidz))
        else:
            purchases = list(Purchase.Query(timeRangeFrom=no,
                                            timeRangeTo=lidz))
            sales = list(Sale.Query(timeRangeFrom=no,
                                    timeRangeTo=lidz))

        return (purchases, sales)

    @staticmethod
    def gvizTransactions(purchases, sales):
        """
        gvizTransactions([x],[y]) -> 'JSON'
        Given a list of sales and a list of transactions, will create a
        JSON string for gviz js library.
        """
        transactions = []
        for purchase in purchases:
            transactions.append([purchase.time, purchase.quantity])

        for sale in sales:
            transactions.append([sale.time, sale.quantity * -1])

        description = [('Laiks', 'datetime'),
                       ('Iepirkts/Pardots', 'number')]

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(transactions)

        jsonified = data_table.ToJSon(columns_order=
                                      ("Laiks", "Iepirkts/Pardots"),
                                      order_by="Laiks")
        return jsonified


class ProductViewer(Handler):
    def get(self):
        # Lego my ego

        ean = self.request.get('ean')
        key = ndb.Key('Product', ean)
        product = key.get()

        periods = self.request.get('periods')
        no = self.request.get('no')
        lidz = self.request.get('lidz')

        no, lidz = Utilities.translateDates(no=no, lidz=lidz, periods=periods)
        purchases, sales = Utilities.getTransactions(no, lidz, key)
        transactionData = Utilities.gvizTransactions(purchases, sales)

        priceIn = product.priceIn if product else 0
        priceOut = product.priceOut if product else 0
        countIn = sum([purchase.quantity for purchase in purchases])
        countOut = sum([sale.quantity for sale in sales])
        expenses = countIn * priceIn
        income = countOut * priceOut

        params = {'product': product,
                  'ean': ean,
                  't': transactionData,
                  'no': no,
                  'lidz': lidz,
                  'countIn': countIn,
                  'countOut': countOut,
                  'income': income,
                  'expenses': expenses
                  }

        self.render('product.html', **params)


class Overview(Handler):
    def get(self):
        periods = self.request.get('periods')
        no = self.request.get('no')
        lidz = self.request.get('lidz')

        no, lidz = Utilities.translateDates(no=no, lidz=lidz, periods=periods)
        purchases, sales = Utilities.getTransactions(no, lidz)

        params = {'no': no,
                  'lidz': lidz,
                  'purchases': purchases,
                  'sales': sales
                  }

        self.render('overview.html', **params)


class PopulateDB(Handler):
    def get(self):
        purchases = []
        eans = ['1234567', '1234568', '3421567', '4321234', '2123459']
        for i in range(1000):

            dt = '2013 ' + str(random.randint(1, 12)).zfill(2) + ' ' +\
                str(random.randint(1, 28)).zfill(2) + ' ' +\
                str(random.randint(8, 18)).zfill(2) + ':' +\
                str(random.randint(0, 59)).zfill(2) + ':' +\
                str(random.randint(0, 59)).zfill(2)

            time = datetime.strptime(dt, '%Y %m %d %H:%M:%S')

            q = {'ean': random.choice(eans),
                 'description': 'Tapete ' + str(random.randint(23450, 99999)) +
                 ' ' + str(random.randint(5, 100)) + 'm rullis',
                 'price': float(random.randint(1, 10)),
                 'quantity': random.randint(1, 15),
                 'time': time}
            purchases.append(q)

        for purchase in purchases:
            Purchase.Process(**purchase)

        sales = []
        for i in range(1000):
            dt = '2013 ' + str(random.randint(1, 12)).zfill(2) + ' ' +\
                str(random.randint(1, 28)).zfill(2) + ' ' +\
                str(random.randint(8, 18)).zfill(2) + ':' +\
                str(random.randint(0, 59)).zfill(2) + ':' +\
                str(random.randint(0, 59)).zfill(2)

            time = datetime.strptime(dt, '%Y %m %d %H:%M:%S')

            q = {'ean': random.choice(eans),
                 'quantity': random.randint(1, 15),
                 'time': time}
            sales.append(q)

        for sale in sales:
            Sale.Process(**sale)

        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/buy', PurchaseHandler),
    ('/sell', SalesHandler),
    ('/parskats', Overview),
    ('/prece', ProductViewer),
    ('/db', PopulateDB),
    ('/', MainPage),
], debug=True)

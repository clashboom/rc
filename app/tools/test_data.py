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

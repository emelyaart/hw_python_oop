import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if today == record.date)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if today >= record.date >= week_ago)

    def add_record(self, record):
        self.records.append(record)

    def get_reminded(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):

    RUB_RATE = 1
    EURO_RATE = 90.53
    USD_RATE = 76.61

    def get_today_cash_remained(self, currency):
        remainder = self.get_reminded()
        if remainder == 0:
            return 'Денег нет, держись'
        currencies = {
            'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        if currency not in currencies:
            keys = ', '.join(list(currencies))
            raise ValueError('Вы ввели "%s", введитe одно из '
                             'следующих значений: %s' % (currency, keys))
        # Спасибо за это :) Незнал этой фишки, либо не запомнил
        currency_rate, currency_name = currencies[currency]
        currency_convert = abs(round(remainder / currency_rate, 2))
        if remainder > 0:
            return ('На сегодня осталось '
                    f'{currency_convert} '
                    f'{currency_name}')
        if remainder < 0:
            return ('Денег нет, держись: твой долг - '
                    f'{currency_convert} '
                    f'{currency_name}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remainder = self.get_reminded()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но '
                    f'с общей калорийностью не более {remainder} кКал')
        return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

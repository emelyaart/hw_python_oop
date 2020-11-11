import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_today_stats(self):
        today = dt.datetime.now().date()
        return sum([record.amount for record in self.records
                    if today == record.date])

    def get_week_stats(self):
        today = dt.datetime.now().date()
        week_ago = today - dt.timedelta(days=7)
        return sum([record.amount for record in self.records
                    if today >= record.date >= week_ago])

    def add_record(self, record):
        self.records.append(record)

    def get_reminded(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):

    EURO_RATE = 90.53
    USD_RATE = 76.61

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        remainder = abs(round(self.get_reminded(), 2))
        remainders = {
            'rub': str(remainder) + ' руб',
            'usd': str(round(remainder / self.USD_RATE, 2)) + ' USD',
            'eur': str(round(remainder / self.EURO_RATE, 2)) + ' Euro'
        }
        if today_stats < self.limit:
            if currency in remainders:
                return 'На сегодня осталось {}'.format(remainders[currency])
            return ("Валюта введена не корректно, введит одно из"
                    " следующих значений: 'rub', 'usd' или 'eur'")
        elif today_stats > self.limit:
            if currency in remainders:
                return 'Денег нет, держись: твой долг - {}'.format(
                    remainders[currency])
        else:
            return 'Денег нет, держись'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        remainder = self.get_reminded()
        if today_stats < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, но '
                    'с общей калорийностью не более {} кКал').format(remainder)
        return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

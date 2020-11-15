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
        # Правильно я Вас понял? С этим возникли сложности :)
        currencies = {
            'rub': (abs(round(remainder / self.RUB_RATE, 2)), 'руб'),
            'usd': (abs(round(remainder / self.USD_RATE, 2)), 'USD'),
            'eur': (abs(round(remainder / self.EURO_RATE, 2)), 'Euro')
        }
        try:
            if currency not in currencies:
                raise ValueError
        except ValueError:
            currencies_key = ', '.join(list(currencies))
            return (f"Вы ввели '{ currency }'', введитe одно из "
                    f"следующих значений: { currencies_key }")
        if remainder == 0:
            return 'Денег нет, держись'
        if remainder > 0:
            return ('На сегодня осталось '
                    f'{ currencies[currency][0] } '
                    f'{ currencies[currency][1] }')
        if remainder < 0:
            return ('Денег нет, держись: твой долг - '
                    f'{ currencies[currency][0] } '
                    f'{ currencies[currency][1] }')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remainder = self.get_reminded()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но '
                    f'с общей калорийностью не более { remainder } кКал')
        return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

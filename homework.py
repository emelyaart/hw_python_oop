import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.datetime.now().date()

    def get_today_stats(self):
        total_today = 0
        for record in self.records:
            if self.today == record.date:
                total_today += record.amount
        return total_today

    def get_week_stats(self):
        total_week = 0
        week_ago = self.today - dt.timedelta(days=7)
        for record in self.records:
            if self.today >= record.date >= week_ago:
                total_week += record.amount
        return total_week

    def add_record(self, record):
        self.records.append(record)


class CashCalculator(Calculator):

    EURO_RATE = 90.53
    USD_RATE = 76.61

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        remainder_rub = abs(round(self.limit - today_stats, 2))
        remainder_usd = round(remainder_rub / self.USD_RATE, 2)
        remainder_euro = round(remainder_rub / self.EURO_RATE, 2)

        if today_stats < self.limit:
            if currency == 'rub':
                return f'На сегодня осталось { remainder_rub } руб'
            elif currency == 'usd':
                return f'На сегодня осталось { remainder_usd } USD'
            elif currency == 'eur':
                return f'На сегодня осталось { remainder_euro } Euro'
        elif today_stats == self.limit:
            return 'Денег нет, держись'
        elif today_stats > self.limit:
            if currency == 'rub':
                return f'Денег нет, держись: твой долг - { remainder_rub } руб'
            elif currency == 'usd':
                return f'Денег нет, держись: твой долг - { remainder_usd } USD'
            elif currency == 'eur':
                return f'Денег нет, держись: твой долг - { remainder_euro } Euro'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        remainder = self.limit - today_stats
        if today_stats < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более { remainder } кКал'
        else:
            return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date == '':
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

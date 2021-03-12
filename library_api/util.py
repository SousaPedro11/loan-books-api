from abc import ABCMeta, abstractmethod
from decimal import Decimal


class Tax:
    __metaclass__ = ABCMeta

    TAX_LESS_THREE_DAYS = None
    TAX_OVER_THREE_DAYS = None
    TAX_OVER_FIVE_DAYS = None

    def __init__(self, days):
        self.loan_days = days

    @abstractmethod
    def calculate(self, **kwargs):
        pass

    def _get_percent_value(self, value: Decimal, tax):
        return value * Decimal(tax)

    def _get_value_delayed(self, value):
        percent_value_three = self._get_percent_value(value, self.TAX_LESS_THREE_DAYS)
        if 0 < self.loan_days <= 3:
            value += percent_value_three
        elif 3 < self.loan_days <= 5:
            value += percent_value_three
            percent_value_five = self._get_percent_value(value, self.TAX_OVER_THREE_DAYS)
            value += percent_value_five
        elif self.loan_days > 5:
            value += percent_value_three
            percent_value_five = self._get_percent_value(value, self.TAX_OVER_THREE_DAYS)
            value += percent_value_five
            percent_value_over = self._get_percent_value(value, self.TAX_OVER_FIVE_DAYS)
            value += percent_value_over
        return value


class Penalty(Tax):
    TAX_LESS_THREE_DAYS = 0.03
    TAX_OVER_THREE_DAYS = 0.05
    TAX_OVER_FIVE_DAYS = 0.07

    def calculate(self, value):
        value = super(Penalty, self)._get_value_delayed(value)
        return value


class InterestPerDay(Tax):
    TAX_LESS_THREE_DAYS = 0.002
    TAX_OVER_THREE_DAYS = 0.004
    TAX_OVER_FIVE_DAYS = 0.006

    def calculate_interest_day(self, value: Decimal, tax: float, day: int):
        return value * ((1 + Decimal(tax)) ** day) - value

    def calculate(self, value: Decimal):
        if 0 < self.loan_days <= 3:
            value += self.calculate_interest_day(value, self.TAX_LESS_THREE_DAYS, self.loan_days)
        elif 3 < self.loan_days <= 5:
            value += self.calculate_interest_day(value, self.TAX_LESS_THREE_DAYS, 3)
            value += self.calculate_interest_day(value, self.TAX_LESS_THREE_DAYS, self.loan_days - 3)
        elif self.loan_days > 5:
            value += self.calculate_interest_day(value, self.TAX_LESS_THREE_DAYS, 3)
            value += self.calculate_interest_day(value, self.TAX_LESS_THREE_DAYS, self.loan_days - 3)
            value += self.calculate_interest_day(value, self.TAX_LESS_THREE_DAYS, self.loan_days - 5)
        return value

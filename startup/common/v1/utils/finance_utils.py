import math
import datetime
from math_utils import positive_ceil, ceil


class LoanCalculator(object):

    def __init__(self, principal, interest_rate, tenure=None, emi=None):
        self.principal = principal
        self.interest_rate = interest_rate
        self.tenure = tenure
        self.emi = emi

    def loan_tenure(self, emi):
        numerator = math.log(
            (emi * 1.0) / (emi - self.principal * self.interest_rate))
        denominator = math.log(1.0 + self.interest_rate)
        return numerator / denominator if (numerator and denominator) else 0

    def loan_tenure_ceiled(self, emi):
        return ceil(self.loan_tenure(emi))

    def loan_emi(self, tenure):
        numerator = self.principal * 1.0 * self.interest_rate
        denominator = (1.0 - (1 + self.interest_rate) ** (-1 * tenure))
        return numerator / denominator if (numerator and denominator) else 0

    def loan_emi_ceiled(self, tenure):
        return ceil(self.loan_emi(tenure))

    def principal_outstanding(self, installment_number):
        return self.principal * ((1 + self.interest_rate)**installment_number) - (((1 + self.interest_rate)**installment_number) - 1) * self.loan_emi(self.tenure) / self.interest_rate

    def principal_outstanding_ceiled(self, installment_number):
        return ceil(self.principal_outstanding(installment_number))

    def interest_paid(self, installment_number):
        return self.principal_outstanding(installment_number) * self.interest_rate

    def interest_paid_ceiled(self, installment_number):
        return ceil(self.interest_paid(installment_number))

    def principal_paid(self, installment_number):
        return self.loan_emi(self.tenure) - self.interest_paid(installment_number)

    def principal_paid_ceiled(self, installment_number):
        return ceil(self.principal_paid(installment_number))

    def rectified_date(self, input_date):
        if input_date.day in [29, 30, 31]:
            if input_date.month == 12:
                return datetime.date(input_date.year + 1, 1, 1)
            else:
                return datetime.date(input_date.year + 1, input_date.month + 1, 1)
        else:
            return input_date

    def safe_next_month_date(self, input_date):
        if input_date.month == 12:
            return datetime.date(input_date.year + 1, 1, input_date.day)
        else:
            return datetime.date(input_date.year, input_date.month + 1, input_date.day)

    def loan_table(self, start_date):
        table_data = []
        installment_date = self.rectified_date(start_date)
        for installment_number in xrange(1, self.tenure + 1):
            installment_date = self.safe_next_month_date(installment_date)
            installment_data = {
                'serial_no': installment_number,
                'emi': self.emi,
                'principal_outstanding': self.principal_outstanding_ceiled(installment_number - 1),
                'principal_paid': self.principal_paid_ceiled(installment_number - 1),
                'interest_paid': self.interest_paid_ceiled(installment_number - 1),
                'due_date': str(installment_date)
            }
            table_data.append(installment_data)
        return table_data


class PenaltyCalulator(object):

    def __init__(self, amount, monthly_interest, monthly_penalty_interest, from_date, on_date=None):
        self.amount = amount
        self.monthly_interest = float(monthly_interest)
        self.monthly_penalty_interest = float(monthly_penalty_interest)
        self.from_date = from_date
        self.on_date = on_date if on_date else datetime.date.today()
        self.penalty = self.__penalty()

    def __penalty(self):
        penalty = 0
        if self.on_date > self.from_date:
            days = (self.on_date - self.from_date).days
            interest_rate = (self.monthly_interest +
                             self.monthly_penalty_interest) / 30
            penalty = ceil(self.amount * days * interest_rate)
        return penalty

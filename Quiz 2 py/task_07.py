
from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_pay(self):
        pass


class SalariedEmployee(Employee):
    def __init__(self, salary):
        self.salary = salary

    def calculate_pay(self):
        return self.salary


class HourlyEmployee(Employee):
    def __init__(self, rate, hours):
        self.rate = rate
        self.hours = hours

    def calculate_pay(self):
        regular = min(self.hours, 40) * self.rate
        overtime = max(0, self.hours - 40) * self.rate * 1.5
        return regular + overtime


class CommissionEmployee(Employee):
    def __init__(self, base, sales, rate):
        self.base = base
        self.sales = sales
        self.rate = rate

    def calculate_pay(self):
        return self.base + self.sales * self.rate


employees = [
    HourlyEmployee(20, 45),
    CommissionEmployee(500, 4000, 0.10)
]

for employee in employees:
    print(employee.calculate_pay())

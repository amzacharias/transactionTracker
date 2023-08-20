"""
Title: Expense clas
Author: Amanda Zacharias
Date Created: 08/12/2023
Date Modified: 08/12/2023
Version: python 3.11
"""

class Transaction: 
    """
    This is a class
    """

    def __init__(self, name, category, amount, denom, date):
        self.name = name
        self.category = category
        self.amount = amount
        self.denom = denom
        self.date = date


    def __repr__(self): 
        # Represent a class object as a string, so we can print(Transaction)
        return f"<Transaction: {self.name}, {self.category}, ${self.amount:.2f}, {self.denom}, {self.date}"
    
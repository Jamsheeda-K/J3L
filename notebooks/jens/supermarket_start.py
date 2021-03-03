"""
Start with this to implement the supermarket simulator.
"""

import numpy as np
import pandas as pd

class Customer:
    """ a single customer, can change state
    """
    def __init__(self, _id, _state):
        self.id = _id
        self.state = _state
    
    def __repr__(self):
        return f'Customer(id={self.id},state={self.state}'

    def next_state(self):
        pass

    def is_active():
        pass

class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0

    def __repr__(self):
        return f'{self.get_time()}: Supermarket with {len(self.customers)}'

    def get_time(self):
        """current time in HH:MM format,
        """
        hour = 7+self.minutes // 60
        minutes = self.minutes % 60
        return f'{hour:02}:{minutes:02}'

    def print_customers(self):
        """print all customers with the current time and id in CSV format.
        """

    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.minutes += 1
        for x in self.customers:
            x.next_state()

    def add_new_customers(self):
        """randomly creates new customers.
        """

    def remove_exitsting_customers(self):
        """removes every customer that is not active any more.
        """

    def is_open(self):
        return self.minutes < 14*60


if(__name__=='__main__'):
    lidl = Supermarket()
    
    while (lidl.is_open()):
        lidl.next_minute()
        lidl.remove_exitsting_customers()
        lidl.add_new_customers()
        print(lidl)

import numpy as np
import pandas as pd
import random

class Customer:
    """a single customer that can be moved from one state to another"""

    def __init__(self, id, initial_state):
        self.id = id
        self.state = initial_state
        #self.budget = budget
        self.matrix = pd.read_csv('trans_matrix.csv',index_col=0)
    

    def __repr__(self):
        return f'<Customer {self.id} in {self.state}>'

    def next_state(self):
        self.state = random.choice(['spices', 'drinks', 'fruit'])

    def is_active(self):
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
        return f'{self.get_time()}: Supermarket with {len(self.customers)} customers.'

    def get_time(self):
        """current time in 'HH:MM' format,
        """
        start_time = 7
        hours = start_time + self.minutes // 60      # integer division
        remainder = self.minutes % 60                # rest
        return f'{hours:02d}:{remainder:02d}:00'


    def print_customers(self):
        """print all customers with the current time and id in CSV format.
        """

    def next_minute(self):
        """propagates all customers to the next state.
        """
        # increase the time of the supermarket by one minute
        self.minutes += 1
        # for every customer move it to their next state
        for customer in self.customers:
            customer.next_state()

    def is_open(self):
        closing_hour = 8
        opening_hour = 7
        # self.get_time() != "21:00"
        return self.minutes < 60*(closing_hour - opening_hour)

    
    def add_new_customers(self):
        """randomly creates new customers.
        """

    def remove_exitsting_customers(self):
        """removes every customer that is not active any more.
        """

# start a simulation
if __name__ == '__main__':
    # this code only runs when we run the file with 'python supermarket.py'
    #lidl = Supermarket()
    cust1 = Customer(1, 'drinks')
    cust1.next_state()

    while lidl.is_open():
        # move on to the next minute
        lidl.next_minute()

        # remove churned customers from the supermarket
        lidl.remove_exitsting_customers()

        # generate new customers at their initial location
        lidl.add_new_customers()

        # repeat from step 1
        print(lidl)


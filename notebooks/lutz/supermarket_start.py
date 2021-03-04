"""
Start with this to implement the supermarket simulator.
"""

import numpy as np
import pandas as pd
class Customer:
    '''a single customer that can move from one state to another'''
    def __init__(self, id, initial_state):
        self.id = id
        self.state = initial_state
    
    def __repr__(self):
        return f'Supermarket with  {len(self.customers)} customers'

    def next_state(self):
        pass

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
        pass

    def get_time():
        """current time in HH:MM format,
        """

    def print_customers():
        """print all customers with the current time and id in CSV format.
        """

    def next_minute():
        """propagates all customers to the next state.
        """
        #increase the time of the supermarket by one minute
        lidl.next_minute
    
    def add_new_customers():
        """randomly creates new customers.
        """

    def remove_exitsting_customers():
        """removes every customer that is not active any more.
        """

# start a simulation

if __name__ == '__main__':
    # this code executed when we run the file python supermarket.py
    lidl = Supermarket()
    print(lidl)


    lidl.next_minute()


    #for every customer determine their next state
    #remove churned customers from the supermarket
    lidl.remove_exitsting_customers()
    #generate new customers at their initial location
    #repeat from step 1
import numpy as np
import pandas as pd
import random

class Customer:
    """a single customer that moves through the supermarket in a MCMC simulation"""

    def __init__(self, name, state, budget=100):
        self.name = name
        self.state = state
        self.budget = budget
    
    def __repr__(self):
        return f'<Customer {self.name} in {self.state}>'
    
    def next_state(self):
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        self.state = random.choice(['spices', 'drinks', 'fruit'])


if __name__ == '__main__':
    #cust1 = Customer()
    cust1 = Customer("Jake", "drinks", 50)
    cust2 = Customer("Margaret", "spices")
    cust1.next_state()
    print(cust1.name, cust1.state)
    print(cust2.name, cust2.budget)

import pandas as pd
import numpy as np
import random


class Customer:
    """a single customer that moves through the supermarket in a MCMC simulation"""

    def __init__(self, id, transition_mat, revenue):
        self.id = id
        self.state = 'in'
        self.transition_mat = transition_mat
        self.revenue  = revenue
        self.count = 0
        self.cost = 0
        self.x = 11
        self.y = 14

    def __repr__(self):
        """
        Returns a csv string for that customer.
        """
        return f'{self.id}:{self.state}'

    def is_active(self):
        """
         Returns True if the customer has not reached the checkout
         for the second time yet, False otherwise.
        """
        return self.state!='out'

    def next_state(self):
        """
        Propagates the customer to the next state
          using a weighted random choice from the transition probabilities
        conditional on the  current state.
          Returns nothing.
        """
        row = self.transition_mat.loc[self.state]
        nstate = random.choices(self.transition_mat.columns, row)
        self.state = nstate[0]
        self.count += 1
        self.cost += self.revenue.get(self.state, 0)

if(__name__=='__main__'):
    df_transition = pd.read_csv('data/freq_table.csv', index_col=0)
    #print(df_transition)
    for i in range(12):
        p1 = Customer(i,df_transition)
        print(p1)
        while(p1.is_active()):
            p1.next_state()
            print(p1)
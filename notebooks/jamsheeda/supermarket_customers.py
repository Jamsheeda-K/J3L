import random
import numpy as np
import create_transition_mat as test

class Customer:

    """a single customer that moves through the supermarket in a MCMC simulation"""

    #churned=False
    def __init__(self, id, state, transition_mat):
        self.id = id
        self.state = state
        self.transition_mat = transition_mat

    def __repr__(self):
        return f'<Customer {self.id} in {self.state}>'

    def next_state(self):
        states = np.array(['entrance','dairy','drinks','fruit','spices','checkout'])
        mat = self.transition_mat.loc[self.state].to_numpy()
        self.state = random.choices(states,mat.transpose())
        print(self.state)


    def is_active(self):
      """
      Returns True if the customer has not reached the checkout
      for the second time yet, False otherwise.
      """
      #if self.state == 'checkout':
          #churned = True

cust1 = Customer('jamz','fruit',test.transition_probability_matrix)
cust1.next_state()
cust1.next_state()
cust1.next_state()
cust1.next_state()
cust1.next_state()
cust1.next_state()
cust1.next_state()
cust1.next_state()
cust1.next_state()


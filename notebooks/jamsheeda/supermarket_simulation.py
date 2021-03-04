"""
Start with this to implement the supermarket simulator.
"""

import numpy as np
import pandas as pd
import random

class Customer:

    """a single customer that moves through the supermarket in a MCMC simulation"""

    def __init__(self, id):
        self.id = id
        self.state = ['entrance']
        self.transition_matrix = pd.read_csv('transition_matrix.csv',index_col=0)

    def __repr__(self):
        return f'<Customer {self.id} in {self.state}>'

    def next_state(self):
        states = np.array(['entrance','dairy','drinks','fruit','spices','checkout'])
        mat = self.transition_matrix.loc[self.state].to_numpy()
        self.state = random.choices(states,mat.transpose())


    def is_active(self):
      """
      Returns True if the customer has not reached the checkout
      for the second time yet, False otherwise.
      """
      if self.state[0] == 'checkout':
          return False
      else:
          return True

class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self,customers,last_id,opening_hour,closing_hour):        
        # a list of Customer objects
        self.customers = customers
        self.minutes = 0
        self.last_id = last_id
        self.transition_matrix = pd.read_csv('transition_matrix.csv',index_col=0)
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        # writing the initial state to a csv file 
        with open('oneday.csv','w') as outfile:
            outfile.write('timestamp;customer_no;location\n')
            for i in range(len(self.customers)):
                outfile.write(f'{self.opening_hour:02d}:00:00;{self.customers[i].id};{self.customers[i].state[0]}\n')


    def __repr__(self):
        return f'{self.get_time()}: Supermarket with {len(self.customers)} customers.'

    def get_time(self):
        """current time in HH:MM format,
        """
        hours = self.opening_hour+self.minutes//60
        remainder = self.minutes % 60
        return f'{hours:02d}:{remainder:02d}:00'

    def print_customers(self):
        """print all customers with the current time and id in CSV format.
        """
        output = ''
        for i in range(len(self.customers)):
            output += f'Customer no. {self.customers[i].id} is in {self.customers[i].state[0]} section\n'
        print(output)
        with open('oneday.csv','a') as outfile:
            for i in range(len(self.customers)):
                outfile.write(f'{self.get_time()};{self.customers[i].id};{self.customers[i].state[0]}\n')

            

    def next_minute(self):
        """propagates all customers to the next state.
        """
        #increase the time of the supermarket by one minute
        self.minutes += 1
        #for every customer determine their next state
        for customer in self.customers:
            customer.next_state()

    def is_open(self):
        return self.minutes < 60*(self.closing_hour-self.opening_hour)
    
    def add_new_customers(self):
        """randomly creates new customers.
        """
        while(len(self.customers)<10) &(self.minutes < 60*(self.closing_hour-self.opening_hour)-5):
            self.customers.append(Customer(self.last_id))
            self.last_id += 1

    def remove_existing_customers(self):
        """removes every customer that is not active any more.
        """

        for i in range(len(self.customers)):
            if self.customers[i].is_active() == False:
                self.customers[i]= 'out'
        self.customers = [item for item in self.customers if item!='out' ]
# start simulation
if __name__=='__main__':
    # this is executed when run the file python supermarket_start.py

    cust_1 = Customer(1)
    cust_2 = Customer(2)
    cust_3 = Customer(3)
    lidl = Supermarket([cust_1,cust_2,cust_3],3,7,7.5)
    #print(lidl)
    while lidl.is_open():
        print(lidl)
        #lidl.print_customers()
        #move to next minute
        lidl.next_minute()
        lidl.print_customers()
        #remove churned customers from the supermarket
        lidl.remove_existing_customers()
        #generate new customers at their initial location
        lidl.add_new_customers()
        #repeat from step 1
        

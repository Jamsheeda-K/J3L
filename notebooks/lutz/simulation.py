"""
Spiced Academy creat a Monte Carlo Markov Chain Simulation

Write a Customer class that represents a single customer in the supermarket.
Uses a transition probability matrix to simulate the journey of a single customer through the market. 
Use a Markov model to represent the state of a customer. 
Use one-minute time intervals for the transitions.
Once a customer reaches the checkout, consider them churned – do not simulate them any longer.
As attributes, the class should take in an id, a transition probability matrix 
(which you extracted earlier from the Data Analysis section) and an initial state:

https://github.com/DanielaMorariu1990/Supermarket_MCMC_simulation/blob/main/supermarket_simulation.py

"""
import time
import datetime
import random
import numpy as np
import pandas as pd
import cv2

#from astar_python.astar import Astar
#from customer_simulation import Customer, dest
#from animation_template import SupermarketMap, MARKET


transition_matrix = pd.read_csv("transition_matrix.csv", index_col=0)
#transition_matrix.set_index("location", inplace=True)
tiles = cv2.imread('tiles.png')

class Customer:
    """a single customer that can be moved from one state to another"""

    def __init__(self, id, initial_state):
        self.id = id
        self.state = initial_state
        #self.budget = budget
        self.matrix = transition_matrix #pd.read_csv('transi_matrix.csv',index_col=0)
    

    def __repr__(self):
        return f'<Customer {self.id} in {self.state}>'

    def next_state(self):
        #print(self.matrix.loc[self.state].to_numpy())
        #self.state = random.choice(['spices', 'drinks', 'fruit', 'dairy','checkout'])
        self.state = random.choices(
            self.matrix.columns,#['entrance','dairy','drinks','fruit','spices','checkout'],
            self.matrix.loc[self.state].to_numpy().T
        )[0]

    def is_active(self):
        pass


class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self, market):        
        # a list of Customer objects
        self.customers = [] # here we need the customer class
        self.minutes = 0 #how many minutes have passed?
        self.id_suffix = 0 # we can concatenate it with the id from customer
        self.possible_states = 5 #or list of locations?
        self.market = market # current supermarket
        self.matrix = transition_matrix #pd.read_csv('trans_matrix.csv',index_col=0)
        self.current_time = 0
        self.opening_hour = 7
        self.closing_hour = 22
    
    
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
        self.current_time = self.get_time()
        return f'Supermarket("{self.customers}", "{self.current_time}")'

    def next_minute(self):
        """propagates all customers to the next state.
        """
        # increase the time of the supermarket by one minute
        self.minutes += 1
        # for every customer move it to their next state
        for customer in self.customers:
            customer.next_state()

    def is_open(self):
        #closing_hour = 8
        #opening_hour = 7
        # self.get_time() != "21:00"
        return self.minutes < 60*(self.closing_hour - self.opening_hour)

    
    def add_new_customers(self): #stop, id_suffix
        """randomly creates new customers.
        """
        while(len(self.customers)<10) &(self.minutes < 60*(self.closing_hour-self.opening_hour)-5):
            self.customers.append(Customer(self.id_suffix, 'entrance'))
            self.id_suffix += 1
        # for i in range(stop):
        #     cust = Customer(str(i) + "_" + str(id_suffix), "entrance", transition_matrix,
        #                     )
        #     self.customers.append(cust)

        # self.id_suffix += 1

    def remove_existing_customers(self):
        """removes every customer that is not active any more.
        """
        # remove the customers which are not active (.is_active )
        self.to_move = False
        #for cust in self.customers:
        #    print(cust.state)
        self.customers = [cust for cust in self.customers if cust.state != 'checkout']
            #if cust.to_move():
            #    self.to_move = True

# start a simulation
if __name__ == '__main__':
    # this code only runs when we run the file with 'python supermarket.py'
    cust1 = Customer(1, 'drinks')
    #cust1.next_state()
    lidl = Supermarket(cust1)
    

    while lidl.is_open():
        # move on to the next minute
        lidl.next_minute()

        # remove churned customers from the supermarket
        lidl.remove_existing_customers()

        # generate new customers at their initial location
        lidl.add_new_customers()

        # repeat from step 1
        #print(lidl)
        print(lidl.print_customers())
        time.sleep(2)

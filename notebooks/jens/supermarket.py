from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from customer import Customer
from copy import copy
import time

#positon of shelves
positions = {'dairy': 2, 'spices':6, 'fruit': 10, 'drinks':14}

#postions in icon file
icon_positions = [4, 1, 2, 3]

#revenue
revenue =  {'dairy': 5, 'spices':3, 'fruit': 4, 'drinks':6}

#probality for not creating a customer now
proba = 0.8

class SuperMarket:
    def __init__(self, data_dir, opening, closing):
        """
        contruct a supermarket with image files in data_dir
        opening and closing hours are integer (0..23)
        """
        im = Image.open(data_dir+'/supermarket.png')
        self.empty_market = np.array(im)
        self.market = copy(self.empty_market)
        im2 = Image.open(data_dir+'/tiles.png')
        self.tiles = np.array(im2)
        im3 = Image.open(data_dir+'/supermarket-icons.png')
        self.icons = np.array(im3)
        self.opening = opening
        self.closing = closing
        self.minutes = 0
        self.customers = []
        self.nextid = 0
        self.transition = pd.read_csv(data_dir+'/../data/freq_table.csv', index_col=0)
        self.income = 0

    def show(self):
        "show the scene in matplotlig window"
        fig = plt.gcf()
        fig.clear()
        plt.imshow(self.market)
        plt.axis('off')
        plt.title(self.__repr__())
        fig.canvas.draw()
        time.sleep(0.5)

    def get_icon(self, x):
        "extract an icon at x (a coordinate pair)"
        step=32
        return self.icons[x[0]*step:(x[0]+1)*step, x[1]*step:(x[1]+1)*step]

    def get_tile(self, x):
        "extract a tile at x (a coordinate pair)"
        step=32
        return self.tiles[x[0]*step:(x[0]+1)*step, x[1]*step:(x[1]+1)*step]

    def set_tile(self, img, x):
        "places a tile into img (numpy-array) at x (a coordinate pair)"
        step=32
        self.market[x[0]*step:(x[0]+1)*step, x[1]*step:(x[1]+1)*step] = img

    def compose(self, places, tiles):
        """places some icons in subermaket, 
        boths args a lists of pairs
        'places' are positons in supermarket (dest)
        'tiles' are postions in tiles images (src)
        """
        self.market = copy(self.empty_market)
        for place,tile in zip(places ,tiles):
            item = self.get_icon(tile)
            self.set_tile(item, place)

    def show_customers(self):
        "place (wo)man icon in correct location, some randomness"
        places = []
        icons = []
        for customer in self.customers:
            if customer.state == 'out':
                continue
            if customer.state == 'in':
                x = 11
                y = 14+random.randint(0,1)
            elif customer.state == 'checkout':
                x = 8
                y = 3+4*+random.randint(0,2)
            else:
                y = positions.get(customer.state,0)+random.randint(0,1)
                x = 2+random.randint(0,4)
            places.append([x,y])
            icons.append([0,0])
        self.compose(places, icons)
        self.show()

    def next_minute(self):
        "move one minute in time"
        self.minutes += 1
        for x in self.customers:
            x.next_state()

    def is_open(self):
        "return False after closing time"
        return self.minutes < 60*(self.closing-self.opening)

    def remove_exitsting_customers(self):
        "remove inactive cosumers from the list"
        new_customer_list = []
        for x in self.customers:
            if(x.is_active()):
                new_customer_list.append(x)
            else:
                self.income += x.cost
        self.customers = new_customer_list

    def add_new_customers(self):
        "randomly add customers to the shop"
        rnd = random.random()
        if(rnd>proba):
            self.customers.append(Customer(self.nextid, self.transition, revenue))
            self.nextid += 1

    def fill_shelves(self):
        "brings icons to the places where the objects are"
        places = []
        icons = []
        for place_shop, place_icon in zip(positions.values(), icon_positions):
            for x in [-1,2]:
                for y in range(5):
                    places.append([2+y, place_shop+x])
                    icons.append([0, place_icon])
        self.compose(places, icons)
        self.show()
        self.empty_market = self.market.copy()

    def get_time(self):
        "returns current time for printing"
        hour = self.minutes // 60
        minutes = self.minutes % 60
        return f'{self.opening+hour:02}:{minutes:02}'

    def __repr__(self):
        "returns a nice string for printing"        
        return f'time={self.get_time()}; #customers={len(self.customers)}; income={self.income}'

    def append_state_to_file(self, fn):
        """
        append the state of the current customers to a csv file 
        at start of simulation file is truncated
        """
        if self.minutes ==0:
            mode = 'w'
        else:
            mode = 'a'
        with open(fn, mode)  as fp:
            for customer in self.customers:
                fp.write(f'{self.get_time()};{customer.id};{customer.state}\n')
        return None

if(__name__=='__main__'):
    doodl = SuperMarket('img', 9, 17)

    fig = plt.gcf()
    fig.show()
    fig.canvas.draw()

    doodl.fill_shelves()
    while (doodl.is_open()):
        doodl.append_state_to_file('simulation.csv')
        doodl.next_minute()
        doodl.remove_exitsting_customers()
        doodl.add_new_customers()
        #print(doodl)
        #if(doodl.minutes % 5 == 0):
        doodl.show_customers()

doodl.append_state_to_file('simulation.csv')
print(f'Supermarkt earned {doodl.income}')
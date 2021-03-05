"supermarket simulations using Monte-Carlo and Markov-chains"
import time
import argparse
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from a_star_adapted import AstarSupermarket
from customer import Customer

try:
    import vlc
    WITH_AUDIO = True
except ModuleNotFoundError:
    WITH_AUDIO = False


#positon of shelves
positions = {'dairy': 2, 'spices':6, 'fruit': 10, 'drinks':14}

#postions in icon file
icon_positions = [4, 1, 2, 3]

#revenue
revenue =  {'dairy': 5, 'spices':3, 'fruit': 4, 'drinks':6}

#PROBAlity for not creating a customer now
PROBA = 0.8

#tile size
TILE_SIZE = 32

class SuperMarket:
    """
    supermarket that allows Monte-Carlo simulations
    """
    def __init__(self, data_dir, opening, closing, astar):
        """
        contruct a supermarket with image files in data_dir
        opening and closing hours are integer (0..23)
        """
        l_im = Image.open(data_dir+'/img/supermarket.png')
        self.empty_market = np.array(l_im)
        self.market = self.empty_market.copy()
        l_im2 = Image.open(data_dir+'/img/tiles.png')
        self.tiles = np.array(l_im2)
        l_im3 = Image.open(data_dir+'/img/supermarket-icons.png')
        self.icons = np.array(l_im3)
        self.opening = opening
        self.closing = closing
        self.do_astar = astar
        self.minutes = 0
        self.customers = []
        self.nextid = 0
        self.transition = pd.read_csv(data_dir+'/data/freq_table.csv', index_col=0)
        self.income = 0
        self.audio = '/home/jkrause/Downloads/kasse.mp3'
        self.astar = AstarSupermarket()

    def show(self):
        "show the scene in matplotlig window"
        l_fig = plt.gcf()
        l_fig.clear()
        plt.imshow(self.market)
        plt.axis('off')
        plt.title(self.__repr__())
        l_fig.canvas.draw()
        time.sleep(0.001)

    def get_icon(self, xy_pos):
        "extract an icon at x (a coordinate pair)"
        x_0 = xy_pos[0]*TILE_SIZE
        x_1 = xy_pos[1]*TILE_SIZE
        return self.icons[x_0:x_0+TILE_SIZE, x_1:x_1+TILE_SIZE]

    def get_tile(self, xy_pos):
        "extract a tile at x (a coordinate pair)"
        x_0 = xy_pos[0]*TILE_SIZE
        x_1 = xy_pos[1]*TILE_SIZE
        return self.tiles[x_0:x_0+TILE_SIZE, x_1:x_1+TILE_SIZE]

    def set_tile(self, img, xy_pos):
        "places a tile into img (numpy-array) at x (a coordinate pair)"
        x_0 = int(xy_pos[0]*TILE_SIZE)
        x_1 = int(xy_pos[1]*TILE_SIZE)
        self.market[x_0:x_0+TILE_SIZE, x_1:x_1+TILE_SIZE] = img

    def compose(self, places, tiles):
        """places some icons in subermaket,
        boths args a lists of pairs
        'places' are positons in supermarket (dest)
        'tiles' are postions in tiles images (src)
        """
        self.market = self.empty_market.copy()
        for place,tile in zip(places ,tiles):
            item = self.get_icon(tile)
            self.set_tile(item, place)

    def sliding_compose(self, oldplaces, places, tiles):
        "slowly move costomer to new location"
        np_oldplaces = np.array(oldplaces, float)
        np_places = np.array(places, float)

        for time_step in np.linspace(0.,1.,16):
            new_places = (1-time_step)*np_oldplaces + time_step*np_places
            self.compose(new_places, tiles)
            self.show()

    def astar_compose(self, oldplaces, places, tiles):
        "move costomers to new location using a* algorithm"
        path_lst = []
        for l_start, l_finish in zip(oldplaces, places):
            l_path = self.astar.find_path(l_start, l_finish)
            path_lst.append(l_path)

        max_len = np.max([len(p) for p in path_lst])
        #print(f'max path = {max_len}')
        for i in range(max_len):
            new_places = []
            for l_path in path_lst:
                if i<len(l_path):
                    new_places.append(l_path[i])
                else:
                    new_places.append(l_path[-1])
            self.compose(new_places, tiles)
            self.show()

    def show_customers(self):
        "place (wo)man icon in correct location, some randomness"
        places = []
        oldplaces = []
        icons = []
        for customer in self.customers:
            if customer.state == 'out':
                continue
            oldplaces.append([customer.pos_x,customer.pos_y])
            if customer.state == 'in':
                customer.pos_x = 11
                customer.pos_y = 14+random.randint(0,1)
                oldplaces[-1] = [customer.pos_x,customer.pos_y]
            elif customer.state == 'checkout':
                customer.pos_x = 8
                customer.pos_y = 3+4*+random.randint(0,2)
            else:
                customer.pos_y = positions.get(customer.state,0)+random.randint(0,1)
                customer.pos_x = 2+random.randint(0,4)
            places.append([customer.pos_x,customer.pos_y])
            icons.append([0,0])
        if len(self.customers)>0:
            if self.do_astar==1:
                self.astar_compose(oldplaces, places, icons)
            else:
                self.sliding_compose(oldplaces, places, icons)
            time.sleep(0.5)
        #self.compose(places, icons)
        #self.show()

    def fill_shelves(self):
        "brings icons to the places where the objects are, randomly leaves some shelves empty"
        places = []
        icons = []
        for place_shop, place_icon in zip(positions.values(), icon_positions):
            for l_x in [-1,2]:
                for l_y in range(5):
                    if random.random()<0.05:
                        continue
                    places.append([2+l_y, place_shop+l_x])
                    icons.append([0, place_icon])
        self.compose(places, icons)
        self.show()
        self.empty_market = self.market.copy()

    def next_minute(self):
        "move one minute in time"
        self.minutes += 1
        for l_cust in self.customers:
            l_cust.next_state()

    def is_open(self):
        "return False after closing time"
        return self.minutes < 60*(self.closing-self.opening)

    def remove_exitsting_customers(self):
        "remove inactive cosumers from the list"
        new_customer_list = []
        for l_cust in self.customers:
            if l_cust.is_active():
                new_customer_list.append(l_cust)
            else:
                self.income += l_cust.cost
                #try:
                #    if WITH_AUDIO:
                #        vlc.MediaPlayer(self.audio).play()
                #except FileNotFoundError:
                #    pass
        self.customers = new_customer_list

    def add_new_customers(self):
        "randomly add customers to the shop"
        rnd = random.random()
        if rnd>PROBA:
            self.customers.append(Customer(self.nextid, self.transition, revenue))
            self.nextid += 1

    def get_time(self):
        "returns current time for printing"
        hour = self.minutes // 60
        minutes = self.minutes % 60
        return f'{self.opening+hour:02}:{minutes:02}'

    def __repr__(self):
        "returns a nice string for printing"
        return f'time={self.get_time()}; #customers={len(self.customers)}; income={self.income}'

    def append_state_to_file(self, f_name):
        """
        append the state of the current customers to a csv file
        at start of simulation file is truncated
        """
        if self.minutes ==0:
            mode = 'w'
        else:
            mode = 'a'
        with open(f_name, mode)  as file_p:
            if self.minutes==0:
                file_p.write('time;customer;location\n')
            for customer in self.customers:
                file_p.write(f'{self.get_time()};{customer.cust_id};{customer.state}\n')


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Supermarket simulator')
    parser.add_argument('-g', '--grafic', help='with graphics',
                        type=int, default = 1, choices=[0,1])
    parser.add_argument('-a', '--astar', help='uses A* algorithm for moving customers',
                        type=int, default = 1, choices=[0,1])
    args = parser.parse_args()

    OUT_FILE = 'simulation.csv'
    doodl = SuperMarket('.', 9, 17, args.astar)

    if args.grafic:
        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()
    else:
        WITH_AUDIO = False

    doodl.fill_shelves()
    try:
        while doodl.is_open():
            doodl.append_state_to_file(OUT_FILE)
            doodl.next_minute()
            doodl.remove_exitsting_customers()
            doodl.add_new_customers()
            if args.grafic:
                doodl.show_customers()
    except KeyboardInterrupt as ex:
        print('Supmarket closes due to illness!')
        #raise ex
doodl.append_state_to_file(OUT_FILE)
print(f'Supermarkt earned {doodl.income}')

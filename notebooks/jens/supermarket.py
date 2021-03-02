from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class SuperMarket:
    def __init__(self, data_dir):
        im = Image.open(data_dir+'/supermarket.png')
        self.empty_market = np.array(im)
        self.market = self.empty_market
        im2 = Image.open(data_dir+'/tiles.png')
        self.tiles = np.array(im2)

    def show(self):
        plt.imshow(self.market)
        plt.axis('off')
        plt.show()

    def get_tile(self, x):
        step=32
        return self.tiles[x[0]*step:(x[0]+1)*step, x[1]*step:(x[1]+1)*step]

    def set_tile(self, img, x):
        step=32
        self.market[x[0]*step:(x[0]+1)*step, x[1]*step:(x[1]+1)*step] = img

    def compose(self, places, tiles):
        self.market = self.empty_market
        for place,tile in zip(places ,tiles):
            item = self.get_tile(tile)
            self.set_tile(item, place)


if(__name__=='__main__'):
    doodl = SuperMarket('img')

    places = [[8,3], [8,7], [8,11]]
    tiles = [[7,0], [7,0], [7,0]]
    doodl.compose(places, tiles)
    doodl.show()


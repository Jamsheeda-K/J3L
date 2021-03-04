'''
### Unicorns
###### properties
- they have a name
- they have a horn in rainbow colors
- they have a mood (happy, positive)
- they have cutie marks
- they have magical powers
##### methods
- they can shit rainbows or fairy dust
- they can fly
- they can attack dinosaurs

### Dinosaurs
##### properties
- they have a mood (depressive, grumpy but also happy, positive)
- they have scales in different colors
- they have one or several horns
##### methods
- they can lay eggs
- they can either eat meat or plants
- they can attack unicorns
'''

import random
import time

# template/ defintion for the object
# class names are CamelCase
class Unicorn:
    
    # constructor function
    def __init__(self, name, strength):
        self.name = name
        # randomly chose happy with 90% probability
        self.mood = random.choices(['happy', 'sad'], [0.9, 0.1])
        self.mood = self.mood[0]
        self.strength = strength

    # called by the print function
    def __repr__(self):
        return f'{self.mood} unicorn with the name {self.name} and of strength {self.strength}'

    # custom method
    def shit(self):
        if self.mood == 'happy':
            print('rainbow')
        else:
            print("sad unicorn don't shit rainbows :(")

class Dinosaur:

    def __init__(self, dinosaur_name, strength):
        self.name = dinosaur_name
        self.strength = strength
        self.number_of_horns = random.randint(0, 5)

    def power(self):
        return self.strength*(self.number_of_horns+1)

    def attack(self, some_unicorn):
        print(f'Dinosaur {self.name} fights against {some_unicorn.name}!')
        time.sleep(3)
        print(f'A heavy fight. {self.name} has {self.number_of_horns} horns.')
        time.sleep(3)
        if self.power() > some_unicorn.strength:
            print('Dinosaur wins.')
        else:
            print('Unicorn wins.')


# create an instance/ object of that class
my_first_unicorn = Unicorn(name='Twilight', strength=100)
other_unicorn = Unicorn('Rainbow Dash', 200)

dino_dinosaur = Dinosaur(name='dino_dinosaur', strength=100)

dino_dinosaur.attack(my_first_unicorn)
dino_dinosaur.attack(other_unicorn)

# print(my_first_unicorn)
# print(my_first_unicorn.name)
# my_first_unicorn.shit()
# print(other_unicorn)
# print(type(my_first_unicorn))

# how to create many dinosaurs at once:

names = ['dino1', 'dino2', 'dino3']
dinosaurs = []
for name in names:
    dinosaurs.append(Dinosaur(name=name, strength=100))


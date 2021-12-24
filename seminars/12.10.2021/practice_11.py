# Animal
    ## Attributes
        ### eating_type (predator, herbivore)
        ### habitat
        ### moving_type
    ## Methods
        ### breathe
        ### eat
        ### sleep


class Animal:
    def __init__(self, eating_type, habitat, moving_type):
        self.eating_type = eating_type
        self.habitat = habitat
        self.moving_type = moving_type

    def breathe(self):
        print('I am breathing...')

    def eat(self, food):
        print(f'I eat {food}')

    def sleep(self, duration):
        print(f'I sleep for {duration} hours')


# Dog
    ## Attributes
        ### eating_type (predator)
        ### tamed (wild, domesticated)
        ### breed
        ### habitat
        ### moving_type
    ## Methods
        ### make_sound
        ### do_command

class Dog(Animal):
    def __init__(self, tamed, breed, habitat):
        self.tamed = tamed
        self.breed = breed
        super().__init__(moving_type='walking', habitat=habitat, eating_type='predator')

    def eat(self, food):
        print(f'I am a Dog. I eat {food}')


pug = Dog('domesticated', 'pug', 'flat')


# Cat
    ## Attributes
        ### eating_type (predator)
        ### habitat
        ### moving_type
        ### character
        ### fluffyness
    ## Methods
        ### sharpen_claws
        ### move_object_from_the_table


class Cat(Animal):
    def __init__(self, habitat, character, fluffiness):
        self.character = character
        self.fluffiness = fluffiness
        super().__init__(eating_type='predator', habitat=habitat, moving_type='walking')


bubble = Cat(habitat='flat', character='playful', fluffiness='very')


animals = [pug, bubble]
for animal in animals:
    animal.eat('meat')

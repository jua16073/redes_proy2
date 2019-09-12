
# Universidad del Valle de Guatemala #
# Redes                              #
# Autores:  Rodrigo Juarez           #
#           Carlos Arroyave          #
#           Michelle Bloomfield      #
# Deck.py: makes a random deck       #

import random


class Deck(object):

    def __init__(self):
        self.card_list = self.generar_cartas()

    def generar_cartas(self):
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        names = [("Two", 15), ("Three", 3), ("Four", 4), ("Five", 5), ("Six", 6), ("Seven", 7), ("Eight", 8), ("Nine", 9), ("Ten", 10), ("J", 11), ("Q", 12),  ("K", 13), ("A", 14)]
        cards = []
        for name in names:
            for suit in suits:
                card = Card(name[0], suit, name[1])
                cards.append(card)
        random.shuffle(cards)
        return cards

    def draw(self):
        return self.card_list.pop()

    def size(self):
        return len(self.card_list)


class Card(object):

    def __init__(self, name, suit, num):
        self.suit = suit
        self.name = name + " of " + suit
        self.num = num

    def get_suit(self):
        return self.suit

    def get_name(self):
        return self.name

    def get_num(self):
        return self.num

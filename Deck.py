
# Universidad del Valle de Guatemala #
# Redes                              #
# Autores:  Rodrigo Juarez           #
#           Carlos Arroyave          #
#           Michelle Bloomfield      #
# Deck.py: makes a random deck       #

import random
class Deck():
    
    def __init__(self):
        self.card_list = self.generar_cartas()

    def generar_cartas(self):
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        names = [("Two", 15), ("Three", 3), ("Four", 4), ("Five", 5), ("Six", 6), ("Seven", 7), ("Eight", 8), ("Nine", 9), ("Ten", 10), ("J", 11), ("Q", 12),  ("K", 13), ("A", 14)]
        cards = []
        for name in names:
            for suit in suits:
                cards.append((name[0], suit, name[1]))
        random.shuffle(cards)
        return cards


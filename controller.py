# Universidad del Valle de Guatemala #
# Redes                              #
# Autores:  Rodrigo Juarez           #
#           Carlos Arroyave          #
#           Michelle Bloomfield      #
# controller.py: control the game    #

import Deck

class Controller():

    def __init__(self):
        self.deck = Deck.Deck()
        self.players = []
        self.game_over = False

    ## Players: list of players that is in the game
    def distribute_cards(self, player):
        return 0
        
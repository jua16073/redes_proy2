# Universidad del Valle de Guatemala #
# Redes                              #
# Autores:  Rodrigo Juarez           #
#           Carlos Arroyave          #
#           Michelle Bloomfield      #
# controller.py: control the game    #

import Deck
import Player

class Controller():

    def __init__(self):
        self.deck = Deck.Deck()
        self.players = []
        self.game_over = False
        self.current_play = []

    ## Players: list of players that is in the game
    def distribute_cards(self, player):
        return 0
        
    def make_move(self):
        return 0

    ## cards: list of cards that the player selects to move
    ## cards: [("Two", 15), ("Three", 3)]
    def valid_move(self, cards):

        ## Validates if the current play has more or equal cards that the player move
        if len(self.current_play)<= len(cards):
            if len(cards)>1:
                ##Si se escogen varias cartas que no son iguales es una movida invalida 
                if(len(set(cards))>1):
                    return False
                
                #### Validar si las cartas anteriores son mayores o iguales que ahorita 
            
            

            



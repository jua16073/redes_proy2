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
        ## current_play: [("Two", 15), ("Three", 3)]
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

            # More than 1 card
            if len(cards)>1:
                ##If the layer has more tha 1 card, it looks if they are the same
                if(len(set(cards))>1):
                    return False
                else: 
                    ## If the last played has the same or less cards that the current play
                    if len(cards)>= len(self.current_play):
                        ##if the played cards are the same or higher then it can be played
                        current_card = self.current_play[0]
                        played_card = cards[0]
                        if(current_card[1]> played_card[1]):
                            return False
                        else: 
                            return True

        ## if the current play has more than the new play then its false
        else: 
            return False

        #Compares the card 
        current_card = self.current_play[0]
        played_card = cards[0]
        if(current_card[1]> played_card[1]):
            return False
        else: 
            return True

            



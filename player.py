# Universidad del Valle de Guatemala                                #
# Redes                                                             #
# Autores:  Rodrigo Juarez                                          #
#           Carlos Arroyave                                         #
#           Michelle Bloomfield                                     #
# Player.py: describes the movements that the player can do         #    


class Player():

	def __init__(self):
		self.cards_left = []
		self.cards_selected = []   

    ## card: card that the player is going to select. 
	def select_card(self, card):
		self.cards_left.remove(card)
		self.cards_selected.append(card)

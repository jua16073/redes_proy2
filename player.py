# Universidad del Valle de Guatemala                                #
# Redes                                                             #
# Autores:  Rodrigo Juarez                                          #
#           Carlos Arroyave                                         #
#           Michelle Bloomfield                                     #
# Player.py: describes the movements that the player can do         #    


class Player():

	def __init__(self, name):
		self.name = name
		self.rank = None
		self.cards_left = []
		self.cards_selected = []   

	# card: card that the player is going to select.
	def select_card(self, card):
		self.cards_left.remove(card)
		self.cards_selected.append(card)

	# cards list of cards that the player have to remove
	def remove_card(self, cards):
		for card in cards:
			self.cards_left.remove(card)

	# cards: list of cards that the player has to add to his hand
	def add_cards(self, cards):
		self.cards_left.append(cards)

	# card: card that is going back to players hand because he made an invalid move
	def invalid_card(self, card):
		self.cards_left.append(card)
		self.cards_selected.remove(card)

	def move(self):
		self.cards_selected = []

	def unselect(self):
		for card in self.cards_selected:
			self.cards_left.append(card)
		self.cards_selected = []

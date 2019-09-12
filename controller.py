# Universidad del Valle de Guatemala #
# Redes                              #
# Autores:  Rodrigo Juarez           #
#           Carlos Arroyave          #
#           Michelle Bloomfield      #
# controller.py: control the president    #

import player


class Controller(object):

    def __init__(self, president):
        self.president = president

    def registration(self):
        name = input('Add new player username: ')
        if name.isalnum():
            p = player.Player(name)
            self.president.add_player(p)
        return not name.isalnum()

    # Players: list of players that is in the president
    def deal_cards(self):
        self.president.deal_cards()
        
    def make_play(self):
        player = self.president.current_turn
        cards = player.cards_selected
        check = self.valid_move()
        if check == "nel":
            self.president.rekterino_playerino()
        elif not self.valid_move():
            print("Invalid Move")
            player.unselect()
        else:
            self.president.make_play()

    def valid_move(self):
        cards_in_play = self.president.current_turn.cards_selected
        cards_in_stack = self.president.carderino
        card_num = cards_in_play[0].num
        for card in cards_in_play:
            if card.num != card_num:
                return False

        if len(cards_in_stack) == 0:
            return True

        cards_in_stack_num = cards_in_stack[0].num
        if cards_in_stack_num > card_num:
            return False

        if cards_in_stack_num == card_num and len(cards_in_stack) == len(cards_in_play):
            return "nel"

        if card_num == 15:
            return len(cards_in_stack) == len(cards_in_play) or len(cards_in_stack) == len(cards_in_play) + 1

        return card_num > cards_in_stack_num and len(cards_in_stack) == len(cards_in_play)


    def move(self):
         print("enter 'pass' to pass your turn or 'unselect' to unselect all cards or ")
         card_name = input("Enter the name of the card you want to select or press Enter to stop selecting: ")
         card_name = card_name.lower()
         player = self.president.current_turn
         cards_name = [card.name.lower() for card in player.cards_left]
         field = self.president.carderino
         if card_name == "unselect":
             self.president.current_turn.unselect()

         elif (card_name == "" and len(player.cards_selected) != 0) or (card_name == "pass" and len(field) != 0):
             return card_name

         elif card_name in cards_name:
             index = cards_name.index(card_name)
             card = player.cards_left[index]
             player.select_card(card)
         else:
             print("INVALID CARD SELECTION")

         return False

    def player_pass(self):
        self.president.current_turn.unselect()
        self.president.passed()





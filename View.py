class View(object):

    def __init__(self, president):

        self.president = president
        self.players = president.players
        self.field = president.carderino
        self.players_in_round = president.current_players
        self.winners = president.winners
        self.curr_turn = president.current_turn
        self.end_game = False

    def update(self):
        self.players = self.president.players
        self.field = self.president.carderino
        self.players_in_round = self.president.current_players
        self.winners = self.president.winners
        self.curr_turn = self.president.current_turn
        self.game_over = self.president.gameover

    def before_start_show(self):
        print ("The current players are: \n" + '\n'.join([player.name for player in self.players]))
        print ("Time to add players, you must add atleast two")

    def show(self):
        print (player.name for player in self.players_in_round)
        print (player.name for player in self.players)
        print ("\n\nThe current cards on the field are: \n" + "\n".join([card.name for card in self.field]))
        print ("\n\n It's " + self.curr_turn.name + " turn:")
        cards = sorted(self.curr_turn.cards_left, key=lambda card: card.num)
        count = 0
        print ("The following are the cards they may play: \n" + "\n".join([card.name for card in cards]))

        selected_cards = self.curr_turn.cards_selected
        print ("\n\nThe following are the cards they have selected: \n" + "\n".join([card.name for card in selected_cards]))

    def show_winners(self):
        print ('\n'.join([player.name for player in self.winners]))

import Deck


class President(object):
    def __init__(self):
        self.deck = Deck.Deck()
        self.players = []
        self.carderino = []
        self.current_players = []
        self.winners = []
        self.current_turn = None
        self.gameover = False

    def add_player(self, player):
        self.players.append(player)

    def check_victory(self):
        player = self.current_turn
        if not len(self.current_turn.cards_left):
            round = self.current_players.index(self.current_turn)
            indexplay = self.players.index(self.current_turn)
            self.next_move()
            self.current_players.pop(round)
            self.players.pop(indexplay)
        return len(player.cards_left) == 0

    def rekterino_playerino(self):
        self.carderino = []
        self.current_turn.move()
        self.check_victory()
        self.gameover = self.end_game()
        self.current_players = self.players[:]

    def passed(self):
        i = self.current_players.index(self.current_turn)
        self.next_move()
        self.current_players.pop(i)
        self.end_round()

    def next_move(self):
        i = self.current_players.index(self.current_turn)
        if i >= len(self.current_players)-1:
            self.current_turn = self.current_players[0]
        else:
            self.current_turn = self.current_players[i+1]

    def end_round(self):
        if len(self.current_players) == 1:
            self.carderino = []
            self.current_players = self.players[:]

    def end_game(self):
        return len(self.players) == 1

    def make_play(self):
        self.carderino = self.current_turn.cards_selected
        self.current_turn.move()
        if not self.check_victory():
            self.next_move()
        self.gameover = self.end_game()

    def deal_cards(self):
        while self.deck.size():
            for player in self.players:
                if self.deck.size() > 0:
                    player.add_cards(self.deck.draw())
        self.current_turn = self.players[0]
        self.current_players = self.players[:]

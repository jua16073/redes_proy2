import President
import View
import controller
import player
import Deck

if __name__ == "__main__":
    game = President.President()
    controller = controller.Controller(game)
    view = View.View(game)
    done_adding = False
    while len(view.players) < 2 or not done_adding:
        view.before_start_show()
        done_adding = controller.registration()
        view.update()
    controller.deal_cards()
    view.update()
    view.show()

    while not view.game_over:
        view.show()
        move = controller.move()
        if move == "pass":
            print ("here")
            controller.player_pass()
        elif move == "":
            controller.make_play()

        view.update()
    view.show_winners()
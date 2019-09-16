import President
import View
import controller
import player
import Deck


class Salas:

    def __init__(self, capacidad):
        self.salas = []
        self.jugadores = []
        self.capacidad = capacidad

    def create_room(self, nombre):
        self.salas.append(Sala(self.capacidad,nombre))
        return self.salas

    def unir_sala(self, jugador, nombre):
        for i in range(0, len(self.salas)):
            if self.salas[i].name() == nombre:
                if self.salas[i].how_many()<4:
                    self.salas[i].jugadores.append(jugador)
                    print(self.salas[i].jugadores_nombres())
                    return self.salas[i].jugadores_nombres()

    def all_salas(self):
        y = []
        for i in range(0,len(self.salas)):
            y.append(self.salas[i].name())
        return y

    def start_game(self, name):
        for i in range(0, len(self.salas)):
            if name in self.salas[i].jugadores_nombres():
                self.salas[i].juego()

class Sala: 

    def __init__(self, capacidad, nombre):
        self.capacidad = capacidad
        self.jugadores = []
        self.nombre = nombre

    def join(self, player):
        if len(self.jugadores) != self.capacidad:
            self.jugadores.append(player)

    def how_many(self):
        return len(self.jugadores)

    def name(self):
        return self.nombre

    def jugadores_nombres(self):
        return self.jugadores
        
    def juego(self):
        game = President.President()
        controllers = controller.Controller(game)
        view = View.View(game)
        controllers.registration(self.jugadores)
        view.update()
        controllers.deal_cards()
        view.update()
        view.show()

        while not view.game_over:
            view.show()
            move = controllers.move()
            if move == "pass":
                print ("here")
                controllers.player_pass()
            elif move == "":
                controllers.make_play()

            view.update()
        view.show_winners()
#import player
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
        self.turn = None
        self.card = None

    def join(self, player):
        if len(self.jugadores) != self.capacidad:
            self.jugadores.append(player)

    def how_many(self):
        return len(self.jugadores)

    def name(self):
        return self.nombre

    def jugadores_nombres(self):
        return self.jugadores
    
    def actuan_turn(self):
        return self.turn

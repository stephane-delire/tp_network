from Host import Host
from Link import Link
from Router import Router
from Packet import Packet

LIGHT_SPEED = 200000000


class Simulator():
    def __init__(self):
        self.hostA = Host()
        self.hostB = Host()
        self.l1 = Link(length=1, speed=1024)
        self.l2 = Link(length=1, speed=1024)
        self.router = Router(queue_max_size=2048)

        self.hostA.attach_link(self.l1)
        self.hostB.attach_link(self.l2)
        self.router.attach_pointA(self.l1)
        self.router.attach_pointB(self.l2)
        self.l1.attach_pointA(self.hostA)
        self.l1.attach_pointB(self.router)
        self.l2.attach_pointA(self.router)
        self.l2.attach_pointB(self.hostB)

    def run(self):
        while self.hostA.queue:
            self.hostA.send_packet(self.hostA.queue[0])
        # debug de la mémoire du routeur :
        #print(self.router)

    def scenario1(self):
        self.hostA.add_packet(Packet(name="1", size=1024))
        self.hostA.add_packet(Packet(name="2", size=1024))
        # Goulot d'étranglement :
        # Diminution de la bande passante de l'hôte récepteur (B)
        self.hostB.bandwidth = 512
        # Comme le routeur à une mémoire de 2048 bits, il peut stocker 2 paquets de 1024 bits.
        # Les paquets 1 et 2 sont donc stockés dans la mémoire du routeur, et la position du
        # deuxième paquet doit être 1.
        self.run()

# Instanciation de la classe Simulator
simulator = Simulator()
# Lancement de la simulation avec le scénario 1
simulator.scenario1()


# Question : 
# Est-ce qu'il faut afficher les packets qui sont drop à la fin de l'ex ? 
# On ne peut pas afficher les lignes plus proprement ?
# Quels sont les valeurs à tester ? 
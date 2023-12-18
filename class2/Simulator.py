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
        self.hostA.add_packet(Packet(name="3", size=1024))
        # Goulot d'étranglement :
        
        self.run()

simulator = Simulator()
simulator.scenario1()


# Question : 
# Est-ce qu'il faut afficher les packets qui sont drop à la fin de l'ex ? 
# On ne peut pas afficher les lignes plus proprement ?
# Quels sont les valeurs à tester ? 
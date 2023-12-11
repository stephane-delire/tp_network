from Host import Host
from Link import Link
from Router import Router
from Packet import Packet


LIGHT_SPEED = 200000000

class Simulator():
    def __init__(self):
        self.hostA = Host("Transmitter")
        self.hostB = Host("Receiver")
        self.l1 = Link(1000, LIGHT_SPEED, 1000000)
        self.l2 = Link(1000, LIGHT_SPEED, 1000000)
        self.router = Router(2048)
        self.hostA.attach_link(self.l1)
        self.hostB.attach_link(self.l2)
        self.router.attach_linkA(self.l1)
        self.router.attach_linkB(self.l2)

    def run(self):
        for packet in self.hostA.queue:
            # Temps de transmission :
            packet.start_time_host = self.hostA.calculate_time(packet)
            self.hostA.remove_packet(packet)
            # Propagation du paquet dans le lien l1
            packet.end_time_router = self.l1.calculate_time(packet) + packet.start_time_host
            self.router.enqueue(packet)
            # Délais de queueing dans le routeur
            packet.start_time_router += self.router.calculate_time(packet) + packet.end_time_router
            self.router.dequeue()
            # Propagation du paquet dans le lien l2
            packet.end_time_host = self.l2.calculate_time(packet) + packet.start_time_router
            self.hostB.add_packet(packet)
            # Temps total
            print("--"*50)
            print("{0} {1} {2} {3} {4}".format(packet.size, packet.start_time_host, packet.end_time_host, packet.pos, packet.dropped))


    def scenario1(self):
        self.hostA.add_packet(Packet(1024))
        self.hostA.add_packet(Packet(1024))
        self.run()


simulator = Simulator()
simulator.scenario1()





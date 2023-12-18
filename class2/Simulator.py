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

        # Valeurs par défaut, utile pour le scénario 3 et 4
        self.nbr_packets = 1
        self.packet_time = 0

    def run(self):
        while self.hostA.queue:
            for i in range(int(self.nbr_packets)):
                if self.hostA.queue:
                    self.hostA.send_packet(self.hostA.queue[0])
                else:
                    break
            # Ajout du temps d'attente au delta de l'hôte émetteur
            self.hostA.delta += self.packet_time

    def scenario1(self):
        """
        Scénario 1 : Goulot d'étranglement
        """
        self.hostA.add_packet(Packet(name="1", size=1024))
        self.hostA.add_packet(Packet(name="2", size=1024))
        # Diminution de la bande passante de l'hôte récepteur (B)
        self.hostB.bandwidth = 512
        # Comme le routeur à une mémoire de 2048 bits, il peut stocker 2 paquets de 1024 bits.
        # Les paquets 1 et 2 sont donc stockés dans la mémoire du routeur, et la position du
        # deuxième paquet doit être 1.
        self.run()

    def scenario2(self):
        """
        Scénario 2 : Goulot d'étranglement avec rejet de paquets
        """
        self.hostA.add_packet(Packet(name="1", size=1024))
        self.hostA.add_packet(Packet(name="2", size=1024))
        # Diminution de la bande passante de l'hôte récepteur (B)
        self.hostB.bandwidth = 512
        # Diminution de la taille de la mémoire du routeur
        self.router.queue_max_size = 1024
        # Comme le routeur à une mémoire de 1024 bits, il ne peut stocker qu'un paquet de 1024 bits.
        # Le paquet 1 est donc jeté par le routeur.
        self.run()

    def scenario3(self):
        """
        Scénario 3 : Goulot d'étranglement sans rejet de paquets.
        L'hôte émetteur doit envoyer les paquets à un intervalle de temps, afin de saturer le lien de sortie du routeur.
        Sans que des paquets soient rejetés par le routeur.
        """
        # Diminution de la bande passante de l'hôte récepteur (B)
        self.hostB.bandwidth = 512
        # Pour ce scénario, la taille des paquets doit être fixe
        packet_size = 1024
        # Il faut calculer l'intervalle de temps entre l'envoi de deux paquets.
        # Afin qu'il n'y ait pas de rejet de paquets, mais que l'hôte récepteur soit
        # toujours en train de recevoir des paquets.
        # L'intervalle de temps à ajouter est : 
        # Délais de transmission de l'hôte récepteur(B) 
        # - 
        # Délais de transmission de l'hôte émetteur(A)
        self.hostA.delta = (packet_size / self.hostB.bandwidth) - (packet_size / self.hostA.bandwidth)
        # On ajoute les paquets à la queue de l'hôte émetteur
        # Dans cette simulation on ajoute 10 paquets.
        for i in range(10):
            self.hostA.add_packet(Packet(name=str(i), size=packet_size))
        # On lance la simulation
        self.run()
    
    def scenario4(self):
        """
        Scénario 4 : Goulot d'étranglement sans rejet de paquets.
        Le scénario 4 est identique au scénario 3, mais fonctionne par rafale.
        C'est la mémoire du routeur qui doit être remplie avant d'envoyer la suite des rafales.
        Les paquets ne doivent pas être rejetés.
        """
        # Diminution de la bande passante de l'hôte récepteur (B)
        self.hostB.bandwidth = 512
        # Pour ce scénario, la taille des paquets doit être fixe
        packet_size = 1024
        # Comme les paquets sont envoyés par rafale, il faut connaître la taille de la mémoire du routeur.
        # Et calculer ainsi le nombre de paquets à envoyer.
        self.nbr_packets = self.router.queue_max_size / packet_size
        # Maintenant il faut calculer le temps que le routeur va prendre pour envoyer les paquets.
        self.packet_time = (packet_size * self.nbr_packets) / self.hostB.bandwidth
        # packet_time sera rajouté au delta de l'hôte émetteur, après chaque rafale.
        # On ajoute les paquets à la queue de l'hôte émetteur
        # Dans cette simulation on ajoute 12 paquets.
        for i in range(12):
            self.hostA.add_packet(Packet(name=str(i), size=packet_size))
        # On lance la simulation
        self.run()
        
    def scenario5(self):
        """
        Scénario 5 : Bonus, envoie aléatoire de paquets.

        """


# Instanciation de la classe Simulator
simulator = Simulator()
# Lancement de la simulation avec le scénario 1
#simulator.scenario1()
# Lancement de la simulation avec le scénario 2
#simulator.scenario2()
# Lancement de la simulation avec le scénario 3
#simulator.scenario3()
# Lancement de la simulation avec le scénario 4
#simulator.scenario4()

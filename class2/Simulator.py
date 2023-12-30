from Host import Host
from Link import Link
from Router import Router
from Packet import Packet
import random

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

        # Valeurs par défaut, utile pour le scénario 4
        self.nbr_packets = 1
        self.packet_time = 0

    def run(self):
        while self.hostA.queue:
            for i in range(int(self.nbr_packets)):
                if self.hostA.queue:
                    self.hostA.send_packet(self.hostA.queue[0])
                else:
                    break
            # Il faut modifier le current_time de l'hôte émetteur
            # Pour simuler son temps d'attente entre rafale de paquets.
            # (scénario 4)
            self.hostA.current_time += self.packet_time

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
        # Il faut calculer l'intervalle de temps entre l'envoi de deux(ou +) paquets.
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
        # Augmentation de la taille de la mémoire du routeur
        # pour qu'il puisse contenir des rafales de 3 paquets de 1024 bits.
        self.router.queue_max_size = 2048 + 1024
        # Comme les paquets sont envoyés par rafale, il faut connaître la taille de la mémoire du routeur.
        # Et calculer ainsi le nombre de paquets à envoyer.
        self.nbr_packets = self.router.queue_max_size / packet_size
        
        # Maintenant il faut calculer le temps que le routeur va prendre pour envoyer les paquets.
        # Le calcul est : 
        self.packet_time = (packet_size / self.hostB.bandwidth) + (packet_size / self.hostA.bandwidth)
        # packet_time sera rajouté au current_time de l'hôte émetteur, après chaque rafale.
        
        # On ajoute les paquets à la queue de l'hôte émetteur
        # Dans cette simulation on ajoute 12 paquets.
        for i in range(12):
            self.hostA.add_packet(Packet(name=str(i), size=packet_size))
        # On lance la simulation
        self.run()
        
    def scenario5(self):
        """
        Scénario 5 : Bonus, envoie aléatoire de paquets.
        
        En ayant des valeurs fixe de vitesse de transfert de données, pour garder un débit constant
        tout en ayant un intervalle de temps aléatoire entre l'envoi de paquets.
        La seule manière est de modifier la taille des paquets... De façon aléatoire, et de calculer
        a chaque fois l'intervalle de temps à ajouter pour ne pas avoir de rejet de paquets.

        Concernant le calcule de la distribution exponentielle, celle-ci se fait en deux étapes :
        1) On génère des nombres aléatoires suivant une distribution exponentielle (positive ou négative)
        2) On normalise ces nombres entre la taille maximum et minimale des paquets.
        --> Voir le fichier distribution_expo.py pour plus de détails.
        Dans ce scénario, nous avons utilisé une distribution exponentielle négative, ce qui privilégie
        les paquets plus gros.

        """
        # Diminution de la bande passante de l'hôte récepteur (B)
        self.hostB.bandwidth = 512
        # nombre de paquet à envoyer (dans cette simulation, 20 paquets car plus simple à visualiser)
        # en cas de doute sur la distribution exponentielle, voir le fichier distribution_expo.py
        nbr_packets = 20
        # taille maximum des paquets
        biggest_packet_size = 1024
        # taille minimum des paquets
        smallest_packet_size = 128
        # On génère les nombres aléatoires suivant une distribution exponentielle
        nums = []
        lbda = -1.5
        for i in range(nbr_packets):
            temp = random.expovariate(lbda) + smallest_packet_size
            nums.append(temp)
        # On normalise les nombres entre la taille maximum et minimale des paquets.
        min_num = min(nums)
        max_num = max(nums)
        for i in range(len(nums)):
            nums[i] = (nums[i] - min_num) / (max_num - min_num) * (biggest_packet_size - smallest_packet_size) + smallest_packet_size
            # Limite de nombre de décimales
            nums[i] = int(round(nums[i], 0))
        # On ajoute les paquets à la queue de l'hôte émetteur
        for i in range(nbr_packets):
            self.hostA.add_packet(Packet(name=str(i), size=nums[i]))
        # On lance la simulation
        self.run()
        # TODO : Calculer l'intervalle de temps entre chaque envoie de paquet
        # pour ne pas jetter de paquets, et avoir un débit constant sur le lien 2.
        



# Instanciation de la classe Simulator
simulator = Simulator()
# Lancement de la simulation avec le scénario 1
#simulator.scenario1()
# Lancement de la simulation avec le scénario 2
#simulator.scenario2()
# Lancement de la simulation avec le scénario 3
#simulator.scenario3()
# Lancement de la simulation avec le scénario 4
simulator.scenario4()
# Lancement de la simulation avec le scénario 5
#simulator.scenario5()
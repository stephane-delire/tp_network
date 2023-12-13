class Host():
    """
    Objet représentant les hôtes du réseau.
    """
    def __init__(self, queue=[], link=None):
        """
        Constructeur de la classe Host.
        """
        self.queue = queue
        # lien par lequel on envoie/reçoit les paquets
        self.link = link
        # Compteur de temps
        self.current_time = 0
        # Vitesse de transmission de l'hôte bits/sec
        self.bandwidth = 1024

    def attach_link(self, link):
        """
        Attache un lien à l'hôte.
        """
        self.link = link

    def add_packet(self, packet):
        """
        Ajoute un paquet à la queue de l'hôte.
        """
        self.queue.append(packet)

    def remove_packet(self, packet):
        """
        Retire un paquet de la queue de l'hôte.
        """
        self.queue.remove(packet)

    def attach_link(self, link):
        """
        Attache un lien à l'hôte.
        """
        self.link = link

    def calculate_time(self, packet):
        """
        Calcule le temps de transmission d'un paquet.
        """
        time = packet.size / self.bandwidth
        return time
    
    def receive_packet(self, packet):
        """
        Reçoit un paquet.
        """
        # Mauvaise idée ça :) ça crée une boucle infinie...
        #self.queue.append(packet)
        print(packet.times)
    def send_packet(self, packet):
        """
        Envoie un paquet.
        """
        print("Host sent a packet !")
        # Initialisation du temps de départ du paquet
        packet.times.append(self.current_time)
        # Ajout du temps de transmission du paquet
        self.current_time += self.calculate_time(packet)
        packet.times.append(self.current_time)
        # Envoie du paquet
        self.link.receive_packet(packet)
        # Retrait du paquet de la queue
        self.remove_packet(packet)

        # Les paquets possèdent 2 temps, le temps de départ 
        # et le temps d'arrivée (délais de transmission).

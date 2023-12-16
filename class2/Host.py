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
        ! Il faut prendre le minimum entre la bandwidth de l'hôte et celle du routeur.
        """
        if self.bandwidth < self.link.pointA.bandwidth:
            time = packet.size / self.bandwidth
        else:
            time = packet.size / self.link.pointA.bandwidth
        return time
    
    def receive_packet(self, packet):
        """
        Reçoit un paquet.
        On imprime les résultats qui sont dans le paquet.
        + Ajout du délais de réception du paquet.
        """

        # Il ne reste que le délais de propagation du lien à ajouter
        # pour avoir le temps total du paquet.
        packet.times.append(packet.times[-1] + self.link.calculate_time(packet))
        

        # Méthode d'affichage des résultats
        print("-"*75)
        print("(" + packet.name + ") ", end=" ")
        for t in packet.times:
            print("|", end=" ")
            t = "{0:.4f}".format(t)
            print(t, end=" ")
        print(" packet.pos : " + str(packet.pos), end=" ")
        print("dropped : " + str(packet.dropped))

    def send_packet(self, packet):
        """
        Envoie un paquet.
        """
        # Initialisation du temps de départ du paquet
        packet.times.append(self.current_time)
        # Ajout du temps de transmission du paquet
        self.current_time += self.calculate_time(packet)
        # Envoie du paquet
        self.link.receive_packet(packet)
        # Retrait du paquet de la queue
        self.remove_packet(packet)
